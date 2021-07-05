from datetime import date, timedelta

from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.cache import cache

from block.serializers import BlockSerializer, BlockDetailsSerializer, BlockTransactionSerializer
from services.block_services import get_blocks, get_block


class ListBlocksApiView(APIView):
    """
    View to list all blocks in the system.

    """
    serializer_class = BlockSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('time',)

    def get(self, request, format=None):
        """
        Return a list of all blocks by time.
        """
        get_data = request.query_params  # or request.GET check both
        yesterday = date.today() - timedelta(days=1)
        yesterday_milliseconds = int(yesterday.strftime("%s")) * 1000
        # make a unique cache key as yesterday timestamp
        cache_key = str(yesterday_milliseconds)

        # Get the existing cache
        blocks = cache.get(cache_key)

        # Fetch blocks from cache ar set it to cache
        if blocks is None:
            blocks = get_blocks(str(yesterday_milliseconds))
            cache.set(cache_key, blocks)
        serializer_before_pagination = BlockSerializer(data=blocks, many=True, context={'request': request})
        if serializer_before_pagination.is_valid():
            serializer_before_pagination_data = [dict(obj) for obj in serializer_before_pagination.data]
            # Filter data if filter is applied
            if get_data.get('search'):
                serializer_before_pagination_data = list(
                    filter(lambda x: get_data.get('search') in x['hash'] or get_data.get('search') in str(
                        x['time_into_datetime']) or get_data.get('search') in str(x['height']) or get_data.get('search') in str(
                        x['block_index']),
                           serializer_before_pagination_data))
            # Sorting data if sorting query param is applied
            if get_data.get('sort_field'):
                sort_field = get_data.get('sort_field')
                order = get_data.get('sort_order')
                serializer_before_pagination_data.sort(key=lambda x: x[sort_field], reverse=order == 'desc')

            # Set Pagination
            # -----------------------------------------------------------
            page_number = self.request.query_params.get('page_number', 1)
            page_size = self.request.query_params.get('page_size', 10)

            paginator = Paginator(serializer_before_pagination_data, page_size)
            serializer = BlockSerializer(paginator.page(page_number), data=serializer_before_pagination_data, many=True,
                                         context={'request': request})
            # -----------------------------------------------------------

            # Apply serializer on our blocks data
            if serializer.is_valid():
                result = {'totalSize': len(serializer_before_pagination_data), 'results': serializer.data}
                return Response(result)
        return Response({})


class DetailBlocksApiView(APIView):
    """
    View the details of a specific block by hash.

    """
    serializer_class = BlockDetailsSerializer

    def get(self, request, *args, **kwargs):
        """
        Return an object with details of a block.
        """
        block_hash = kwargs.get('hash')
        # Get the existing cache by key as hash
        block_details = cache.get(block_hash)
        # Get block details from cache or set it
        if block_details is None:
            block_details = get_block(block_hash)
            cache.set(block_hash, block_details)

        # Apply serializer on our block details data
        serializer = BlockDetailsSerializer(data=block_details)
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
        # Get the existing cache
        block_details = cache.get(block_hash)
        # Get block transactions list from cache or set it
        if block_details is None:
            block_details = get_block(block_hash)
            cache.set(block_hash, block_details)

        serializer_before_pagination = BlockTransactionSerializer(data=block_details['tx'], many=True, context={'request': request})
        if serializer_before_pagination.is_valid():
            serializer_before_pagination_data = [dict(obj) for obj in serializer_before_pagination.data]
            # Filter data if search query param is applied
            if self.request.query_params.get('search'):
                search_query = self.request.query_params.get('search')
                serializer_before_pagination_data = list(
                    filter(lambda x: search_query in x['hash'] or search_query in str(
                        x['time_into_datetime']) or search_query in str(x['size']) or search_query in str(
                        x['weight']) or search_query in str(x['fee']),
                           serializer_before_pagination_data))

            # Sort data if sort_field is applied
            if self.request.query_params.get('sort_field'):
                sort_field = self.request.query_params.get('sort_field')
                order = self.request.query_params.get('sort_order')
                serializer_before_pagination_data.sort(key=lambda x: x[sort_field], reverse=order == 'desc')

            # Pagination
            # -----------------------------------------------------------
            page_number = self.request.query_params.get('page_number', 1)
            page_size = self.request.query_params.get('page_size', 10)

            paginator = Paginator(serializer_before_pagination_data, page_size)

            # -----------------------------------------------------------
            # Apply serializer
            serializer = BlockTransactionSerializer(paginator.page(page_number), data=serializer_before_pagination_data, many=True)
            if serializer.is_valid():
                result = {'totalSize': len(serializer_before_pagination_data), 'results': serializer.data}
                return Response(result)
        return Response({})
