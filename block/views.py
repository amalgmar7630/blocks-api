from datetime import date, timedelta

from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from block.serializers import BlockSerializer, BlockDetailsSerializer, BlockTransactionSerializer
from services.block_services import get_blocks, get_block


class ListBlocksApiView(APIView):
    """
    View to list all blocks-api in the system.

    """
    serializer_class = BlockSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('time',)

    def get(self, request, format=None):
        """
        Return a list of all blocks-api by time.
        """
        get_data = request.query_params  # or request.GET check both
        yesterday = date.today() - timedelta(days=1)
        yesterday_milliseconds = int(yesterday.strftime("%s")) * 1000
        blocks = get_blocks(str(get_data.get('time'))) if get_data.get('time') else get_blocks(
            str(yesterday_milliseconds))
        if get_data.get('search'):
            blocks = list(
                filter(lambda x: get_data.get('search') in x['hash'] or get_data.get('search') in str(
                    x['time']) or get_data.get('search') in str(x['height']) or get_data.get('search') in str(
                    x['block_index']),
                       blocks))
        # -----------------------------------------------------------
        page_number = self.request.query_params.get('page_number', 1)
        page_size = self.request.query_params.get('page_size', 10)

        paginator = Paginator(blocks, page_size)
        serializer = BlockSerializer(paginator.page(page_number), data=blocks, many=True, context={'request': request})
        # -----------------------------------------------------------
        if serializer.is_valid():
            result = {'totalSize': len(blocks), 'results': serializer.data}
            return Response(result)
        return Response({})


class DetailBlocksApiView(APIView):
    """
    View the details of a specific block bu hash.

    """
    serializer_class = BlockDetailsSerializer

    def get(self, request, *args, **kwargs):
        """
        Return an object with details of a block.
        """
        block_hash = kwargs.get('hash')
        block = get_block(block_hash)
        serializer = BlockDetailsSerializer(data=block)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response({})


class ListTransactionsApiView(APIView):
    """
    View the transactions of a specific block.

    """
    serializer_class = BlockTransactionSerializer

    def get(self, request, *args, **kwargs):
        """
        Return a list with all the transactions.
        """
        block_hash = kwargs.get('hash')
        block = get_block(block_hash)
        if self.request.query_params.get('search'):
            search_query = self.request.query_params.get('search')
            block['tx'] = list(
                filter(lambda x: search_query in x['hash'] or search_query in str(
                    x['time']) or search_query in str(x['size']) or search_query in str(
                    x['weight']) or search_query in str(x['fee']),
                       block['tx']))
        # -----------------------------------------------------------
        page_number = self.request.query_params.get('page_number', 1)
        page_size = self.request.query_params.get('page_size', 10)

        paginator = Paginator(block['tx'], page_size)
        serializer = BlockTransactionSerializer(paginator.page(page_number), data=block['tx'], many=True)

        # -----------------------------------------------------------
        if serializer.is_valid():
            result = {'totalSize': len(block['tx']), 'results': serializer.data}
            return Response(result)
        return Response({})
