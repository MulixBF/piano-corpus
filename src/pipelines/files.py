from scrapy.pipelines.files import FilesPipeline, FileException
from scrapy.http import Response
import logging
import requests

from scrapy.utils.request import referer_str

logger = logging.getLogger(__name__)


class FilesPipelineWithRedirect(FilesPipeline):
    """
    Kludge. See https://github.com/scrapy/scrapy/issues/2004
    There is a pull request pending since August: https://github.com/scrapy/scrapy/pull/2193
    """

    def media_downloaded(self, response, request, info):

        referer = referer_str(request)

        # Synchronous request inside pipeline. What idiot wrote this? ;)
        if response.status == 301 or response.status == 302:
            logger.info('Following redirect in %s', request)
            redirect_location = response.headers['Location'].decode()
            r = requests.get(redirect_location)
            response = Response(redirect_location, status=r.status_code, body=r.content, request=request)
            logger.info('Followed redirect. Result: %s', str(response))

        if response.status != 200:
            logger.warning(
                'File (code: %(status)s): Error downloading file from '
                '%(request)s referred in <%(referer)s>',
                {'status': response.status,
                 'request': request, 'referer': referer},
                extra={'spider': info.spider}
            )
            raise FileException('download-error')

        if not response.body:
            logger.warning(
                'File (empty-content): Empty file from %(request)s referred '
                'in <%(referer)s>: no-content',
                {'request': request, 'referer': referer},
                extra={'spider': info.spider}
            )
            raise FileException('empty-content')

        status = 'cached' if 'cached' in response.flags else 'downloaded'
        logger.debug(
            'File (%(status)s): Downloaded file from %(request)s referred in '
            '<%(referer)s>',
            {'status': status, 'request': request, 'referer': referer},
            extra={'spider': info.spider}
        )
        self.inc_stats(info.spider, status)

        try:
            path = self.file_path(request, response=response, info=info)
            checksum = self.file_downloaded(response, request, info)
        except FileException as exc:
            logger.warning(
                'File (error): Error processing file from %(request)s '
                'referred in <%(referer)s>: %(errormsg)s',
                {'request': request, 'referer': referer, 'errormsg': str(exc)},
                extra={'spider': info.spider}, exc_info=True
            )
            raise
        except Exception as exc:
            logger.error(
                'File (unknown-error): Error processing file from %(request)s '
                'referred in <%(referer)s>',
                {'request': request, 'referer': referer},
                exc_info=True, extra={'spider': info.spider}
            )
            raise FileException(str(exc))

        return {'url': request.url, 'path': path, 'checksum': checksum}
