#!/usr/bin/env python3
"""
PrestaShop MCP Server (FastMCP)
Universal MCP server for PrestaShop Web Services API (reporting focus)
Refactored to use FastMCP pattern (December 2025)
"""

from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import sys
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
import httpx

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get environment variables
CLIENTS_BASE_PATH = os.environ.get(
    "CLIENTS_BASE_PATH",
    "/Users/administrator/Documents/PetesBrain.nosync/clients"
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('prestashop-mcp')

# Initialize FastMCP
mcp = FastMCP("PrestaShop Tools")

# Server startup
logger.info("Starting PrestaShop MCP Server (FastMCP)...")
logger.info(f"Clients base path: {CLIENTS_BASE_PATH}")


# ============================================================================
# PrestaShop API Client
# ============================================================================

class PrestaShopClient:
    """Client for PrestaShop Web Services API"""

    def __init__(self, shop_url: str, api_key: str):
        """
        Initialize PrestaShop client

        Args:
            shop_url: PrestaShop shop URL (e.g., https://yourshop.com)
            api_key: PrestaShop Web Services API key
        """
        self.shop_url = shop_url.rstrip('/')
        self.api_url = f"{self.shop_url}/api"
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            auth=(api_key, ''),  # PrestaShop uses Basic Auth with API key as username
            timeout=30.0
        )

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> ET.Element:
        """
        Make GET request to PrestaShop API

        Args:
            endpoint: API endpoint (e.g., 'products', 'orders')
            params: Query parameters

        Returns:
            XML Element tree root
        """
        url = f"{self.api_url}/{endpoint}"

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()

            # Parse XML response
            root = ET.fromstring(response.content)
            return root

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise

    async def get_products(
        self,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        filter_params: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Get products with optional filtering

        Args:
            limit: Maximum number of products to return
            sort: Sort field (e.g., 'id_ASC', 'name_DESC')
            filter_params: Filter parameters (e.g., {'active': '1'})

        Returns:
            List of product dictionaries
        """
        params = {'display': 'full'}

        if limit:
            params['limit'] = str(limit)
        if sort:
            params['sort'] = sort
        if filter_params:
            # PrestaShop filter format: filter[field]=[value]
            for key, value in filter_params.items():
                params[f'filter[{key}]'] = value

        root = await self._get('products', params)

        products = []
        for product_elem in root.findall('.//product'):
            product = self._parse_product(product_elem)
            products.append(product)

        return products

    async def get_product(self, product_id: str) -> Dict:
        """
        Get single product by ID

        Args:
            product_id: Product ID

        Returns:
            Product dictionary
        """
        root = await self._get(f'products/{product_id}')
        product_elem = root.find('.//product')
        return self._parse_product(product_elem)

    async def get_orders(
        self,
        limit: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        filter_params: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Get orders with optional filtering

        Args:
            limit: Maximum number of orders to return
            date_from: Start date (YYYY-MM-DD format)
            date_to: End date (YYYY-MM-DD format)
            filter_params: Additional filter parameters

        Returns:
            List of order dictionaries
        """
        params = {'display': 'full'}

        if limit:
            params['limit'] = str(limit)

        # Date filtering
        if date_from or date_to:
            if not filter_params:
                filter_params = {}

            if date_from and date_to:
                filter_params['invoice_date'] = f'[{date_from} 00:00:00,{date_to} 23:59:59]'
            elif date_from:
                filter_params['invoice_date'] = f'>[{date_from} 00:00:00]'
            elif date_to:
                filter_params['invoice_date'] = f'<[{date_to} 23:59:59]'

        if filter_params:
            for key, value in filter_params.items():
                params[f'filter[{key}]'] = value

        root = await self._get('orders', params)

        orders = []
        for order_elem in root.findall('.//order'):
            order = self._parse_order(order_elem)
            orders.append(order)

        return orders

    async def get_order(self, order_id: str) -> Dict:
        """
        Get single order by ID

        Args:
            order_id: Order ID

        Returns:
            Order dictionary
        """
        root = await self._get(f'orders/{order_id}')
        order_elem = root.find('.//order')
        return self._parse_order(order_elem)

    async def get_order_details(self, order_id: str) -> List[Dict]:
        """
        Get order line items

        Args:
            order_id: Order ID

        Returns:
            List of order detail dictionaries
        """
        params = {
            'display': 'full',
            'filter[id_order]': order_id
        }

        root = await self._get('order_details', params)

        details = []
        for detail_elem in root.findall('.//order_detail'):
            detail = self._parse_order_detail(detail_elem)
            details.append(detail)

        return details

    async def get_customers(
        self,
        limit: Optional[int] = None,
        filter_params: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Get customers with optional filtering

        Args:
            limit: Maximum number of customers to return
            filter_params: Filter parameters

        Returns:
            List of customer dictionaries
        """
        params = {'display': 'full'}

        if limit:
            params['limit'] = str(limit)
        if filter_params:
            for key, value in filter_params.items():
                params[f'filter[{key}]'] = value

        root = await self._get('customers', params)

        customers = []
        for customer_elem in root.findall('.//customer'):
            customer = self._parse_customer(customer_elem)
            customers.append(customer)

        return customers

    async def get_categories(self) -> List[Dict]:
        """
        Get all product categories

        Returns:
            List of category dictionaries
        """
        params = {'display': 'full'}
        root = await self._get('categories', params)

        categories = []
        for category_elem in root.findall('.//category'):
            category = self._parse_category(category_elem)
            categories.append(category)

        return categories

    async def get_stock_availables(
        self,
        product_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Get stock availability information

        Args:
            product_id: Optional product ID to filter by

        Returns:
            List of stock availability dictionaries
        """
        params = {'display': 'full'}

        if product_id:
            params['filter[id_product]'] = product_id

        root = await self._get('stock_availables', params)

        stocks = []
        for stock_elem in root.findall('.//stock_available'):
            stock = self._parse_stock_available(stock_elem)
            stocks.append(stock)

        return stocks

    def _parse_product(self, elem: ET.Element) -> Dict:
        """Parse product XML element to dictionary"""
        return {
            'id': elem.find('id').text if elem.find('id') is not None else None,
            'name': self._get_language_field(elem, 'name'),
            'reference': elem.find('reference').text if elem.find('reference') is not None else None,
            'price': elem.find('price').text if elem.find('price') is not None else None,
            'wholesale_price': elem.find('wholesale_price').text if elem.find('wholesale_price') is not None else None,
            'active': elem.find('active').text if elem.find('active') is not None else None,
            'quantity': elem.find('quantity').text if elem.find('quantity') is not None else None,
            'id_category_default': elem.find('id_category_default').text if elem.find('id_category_default') is not None else None,
            'date_add': elem.find('date_add').text if elem.find('date_add') is not None else None,
            'date_upd': elem.find('date_upd').text if elem.find('date_upd') is not None else None,
        }

    def _parse_order(self, elem: ET.Element) -> Dict:
        """Parse order XML element to dictionary"""
        return {
            'id': elem.find('id').text if elem.find('id') is not None else None,
            'id_customer': elem.find('id_customer').text if elem.find('id_customer') is not None else None,
            'reference': elem.find('reference').text if elem.find('reference') is not None else None,
            'current_state': elem.find('current_state').text if elem.find('current_state') is not None else None,
            'total_paid': elem.find('total_paid').text if elem.find('total_paid') is not None else None,
            'total_paid_tax_incl': elem.find('total_paid_tax_incl').text if elem.find('total_paid_tax_incl') is not None else None,
            'total_paid_tax_excl': elem.find('total_paid_tax_excl').text if elem.find('total_paid_tax_excl') is not None else None,
            'total_products': elem.find('total_products').text if elem.find('total_products') is not None else None,
            'total_products_wt': elem.find('total_products_wt').text if elem.find('total_products_wt') is not None else None,
            'total_shipping': elem.find('total_shipping').text if elem.find('total_shipping') is not None else None,
            'payment': elem.find('payment').text if elem.find('payment') is not None else None,
            'date_add': elem.find('date_add').text if elem.find('date_add') is not None else None,
            'date_upd': elem.find('date_upd').text if elem.find('date_upd') is not None else None,
            'invoice_date': elem.find('invoice_date').text if elem.find('invoice_date') is not None else None,
        }

    def _parse_order_detail(self, elem: ET.Element) -> Dict:
        """Parse order detail XML element to dictionary"""
        return {
            'id': elem.find('id').text if elem.find('id') is not None else None,
            'id_order': elem.find('id_order').text if elem.find('id_order') is not None else None,
            'product_id': elem.find('product_id').text if elem.find('product_id') is not None else None,
            'product_name': elem.find('product_name').text if elem.find('product_name') is not None else None,
            'product_reference': elem.find('product_reference').text if elem.find('product_reference') is not None else None,
            'product_quantity': elem.find('product_quantity').text if elem.find('product_quantity') is not None else None,
            'product_price': elem.find('product_price').text if elem.find('product_price') is not None else None,
            'unit_price_tax_incl': elem.find('unit_price_tax_incl').text if elem.find('unit_price_tax_incl') is not None else None,
            'unit_price_tax_excl': elem.find('unit_price_tax_excl').text if elem.find('unit_price_tax_excl') is not None else None,
            'total_price_tax_incl': elem.find('total_price_tax_incl').text if elem.find('total_price_tax_incl') is not None else None,
            'total_price_tax_excl': elem.find('total_price_tax_excl').text if elem.find('total_price_tax_excl') is not None else None,
        }

    def _parse_customer(self, elem: ET.Element) -> Dict:
        """Parse customer XML element to dictionary"""
        return {
            'id': elem.find('id').text if elem.find('id') is not None else None,
            'email': elem.find('email').text if elem.find('email') is not None else None,
            'firstname': elem.find('firstname').text if elem.find('firstname') is not None else None,
            'lastname': elem.find('lastname').text if elem.find('lastname') is not None else None,
            'active': elem.find('active').text if elem.find('active') is not None else None,
            'date_add': elem.find('date_add').text if elem.find('date_add') is not None else None,
            'date_upd': elem.find('date_upd').text if elem.find('date_upd') is not None else None,
        }

    def _parse_category(self, elem: ET.Element) -> Dict:
        """Parse category XML element to dictionary"""
        return {
            'id': elem.find('id').text if elem.find('id') is not None else None,
            'name': self._get_language_field(elem, 'name'),
            'active': elem.find('active').text if elem.find('active') is not None else None,
            'id_parent': elem.find('id_parent').text if elem.find('id_parent') is not None else None,
            'level_depth': elem.find('level_depth').text if elem.find('level_depth') is not None else None,
        }

    def _parse_stock_available(self, elem: ET.Element) -> Dict:
        """Parse stock_available XML element to dictionary"""
        return {
            'id': elem.find('id').text if elem.find('id') is not None else None,
            'id_product': elem.find('id_product').text if elem.find('id_product') is not None else None,
            'id_product_attribute': elem.find('id_product_attribute').text if elem.find('id_product_attribute') is not None else None,
            'quantity': elem.find('quantity').text if elem.find('quantity') is not None else None,
            'depends_on_stock': elem.find('depends_on_stock').text if elem.find('depends_on_stock') is not None else None,
            'out_of_stock': elem.find('out_of_stock').text if elem.find('out_of_stock') is not None else None,
        }

    def _get_language_field(self, elem: ET.Element, field_name: str) -> Optional[str]:
        """Extract language field value (PrestaShop uses language nodes)"""
        field = elem.find(field_name)
        if field is not None:
            # Try to get English version first, otherwise get first available
            lang_elem = field.find(".//language[@id='1']")
            if lang_elem is None:
                lang_elem = field.find('.//language')
            if lang_elem is not None:
                return lang_elem.text
        return None

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# ============================================================================
# Helper Functions
# ============================================================================

def get_client_credentials(client_name: str) -> Dict[str, str]:
    """
    Get PrestaShop credentials from client CONTEXT.md

    Args:
        client_name: Client name (normalized to lowercase with hyphens)

    Returns:
        Dictionary with shop_url and api_key
    """
    # Normalise client name
    client_name = client_name.lower().replace(' ', '-')

    # Path to client CONTEXT.md
    context_path = Path(f"{CLIENTS_BASE_PATH}/{client_name}/CONTEXT.md")

    if not context_path.exists():
        raise FileNotFoundError(f"CONTEXT.md not found for client: {client_name}")

    # Parse CONTEXT.md for PrestaShop credentials
    with open(context_path) as f:
        content = f.read()

    credentials = {}

    # Look for PrestaShop section
    lines = content.split('\n')
    in_prestashop_section = False

    for line in lines:
        if '## PrestaShop' in line or '### PrestaShop' in line:
            in_prestashop_section = True
            continue

        if in_prestashop_section:
            # Stop at next section
            if line.startswith('##') or line.startswith('###'):
                break

            # Extract credentials
            if 'Shop URL:' in line:
                credentials['shop_url'] = line.split('Shop URL:')[1].strip().strip('`')
            elif 'API Key:' in line:
                credentials['api_key'] = line.split('API Key:')[1].strip().strip('`')

    if not credentials.get('shop_url') or not credentials.get('api_key'):
        raise ValueError(
            f"PrestaShop credentials not found in CONTEXT.md for {client_name}. "
            "Please add PrestaShop section with Shop URL and API Key."
        )

    return credentials


# ============================================================================
# MCP Tools (FastMCP Pattern)
# ============================================================================

@mcp.tool
async def get_orders(
    client_name: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 100,
    ctx: Context = None
) -> str:
    """
    Get orders from PrestaShop for a specific client.

    Args:
        client_name: Client name (e.g., 'accessories-for-the-home')
        date_from: Optional start date (YYYY-MM-DD format)
        date_to: Optional end date (YYYY-MM-DD format)
        limit: Maximum number of orders (default: 100)

    Returns:
        JSON string with list of orders
    """
    try:
        # Get credentials from CONTEXT.md
        creds = get_client_credentials(client_name)

        # Create client and fetch orders
        client = PrestaShopClient(creds['shop_url'], creds['api_key'])
        try:
            orders = await client.get_orders(
                limit=limit,
                date_from=date_from,
                date_to=date_to
            )
            return f"Found {len(orders)} orders\n\n" + str(orders)
        finally:
            await client.close()

    except Exception as e:
        logger.error(f"Error fetching orders for {client_name}: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool
async def get_order(
    client_name: str,
    order_id: str,
    ctx: Context = None
) -> str:
    """
    Get a single order with line items.

    Args:
        client_name: Client name (e.g., 'accessories-for-the-home')
        order_id: Order ID

    Returns:
        JSON string with order details and line items
    """
    try:
        creds = get_client_credentials(client_name)
        client = PrestaShopClient(creds['shop_url'], creds['api_key'])
        try:
            order = await client.get_order(order_id)
            order_details = await client.get_order_details(order_id)
            result = {
                "order": order,
                "line_items": order_details
            }
            return str(result)
        finally:
            await client.close()

    except Exception as e:
        logger.error(f"Error fetching order {order_id} for {client_name}: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool
async def get_products(
    client_name: str,
    limit: int = 100,
    active_only: bool = False,
    sort: Optional[str] = None,
    ctx: Context = None
) -> str:
    """
    Get products from PrestaShop.

    Args:
        client_name: Client name (e.g., 'accessories-for-the-home')
        limit: Maximum number of products (default: 100)
        active_only: Filter for active products only (default: False)
        sort: Optional sort field (e.g., 'id_ASC', 'name_DESC', 'price_ASC')

    Returns:
        JSON string with list of products
    """
    try:
        creds = get_client_credentials(client_name)
        client = PrestaShopClient(creds['shop_url'], creds['api_key'])

        filter_params = {}
        if active_only:
            filter_params['active'] = '1'

        try:
            products = await client.get_products(
                limit=limit,
                sort=sort,
                filter_params=filter_params if filter_params else None
            )
            return f"Found {len(products)} products\n\n" + str(products)
        finally:
            await client.close()

    except Exception as e:
        logger.error(f"Error fetching products for {client_name}: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool
async def get_product(
    client_name: str,
    product_id: str,
    ctx: Context = None
) -> str:
    """
    Get a single product by ID.

    Args:
        client_name: Client name (e.g., 'accessories-for-the-home')
        product_id: Product ID

    Returns:
        JSON string with product details
    """
    try:
        creds = get_client_credentials(client_name)
        client = PrestaShopClient(creds['shop_url'], creds['api_key'])
        try:
            product = await client.get_product(product_id)
            return str(product)
        finally:
            await client.close()

    except Exception as e:
        logger.error(f"Error fetching product {product_id} for {client_name}: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool
async def get_customers(
    client_name: str,
    limit: int = 100,
    active_only: bool = False,
    ctx: Context = None
) -> str:
    """
    Get customers from PrestaShop.

    Args:
        client_name: Client name (e.g., 'accessories-for-the-home')
        limit: Maximum number of customers (default: 100)
        active_only: Filter for active customers only (default: False)

    Returns:
        JSON string with list of customers
    """
    try:
        creds = get_client_credentials(client_name)
        client = PrestaShopClient(creds['shop_url'], creds['api_key'])

        filter_params = {}
        if active_only:
            filter_params['active'] = '1'

        try:
            customers = await client.get_customers(
                limit=limit,
                filter_params=filter_params if filter_params else None
            )
            return f"Found {len(customers)} customers\n\n" + str(customers)
        finally:
            await client.close()

    except Exception as e:
        logger.error(f"Error fetching customers for {client_name}: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool
async def get_categories(
    client_name: str,
    ctx: Context = None
) -> str:
    """
    Get all product categories.

    Args:
        client_name: Client name (e.g., 'accessories-for-the-home')

    Returns:
        JSON string with list of categories
    """
    try:
        creds = get_client_credentials(client_name)
        client = PrestaShopClient(creds['shop_url'], creds['api_key'])
        try:
            categories = await client.get_categories()
            return f"Found {len(categories)} categories\n\n" + str(categories)
        finally:
            await client.close()

    except Exception as e:
        logger.error(f"Error fetching categories for {client_name}: {str(e)}")
        return f"Error: {str(e)}"


@mcp.tool
async def get_stock_levels(
    client_name: str,
    product_id: Optional[str] = None,
    ctx: Context = None
) -> str:
    """
    Get stock availability for products.

    Args:
        client_name: Client name (e.g., 'accessories-for-the-home')
        product_id: Optional product ID to filter by

    Returns:
        JSON string with stock availability information
    """
    try:
        creds = get_client_credentials(client_name)
        client = PrestaShopClient(creds['shop_url'], creds['api_key'])
        try:
            stocks = await client.get_stock_availables(product_id)
            return f"Found {len(stocks)} stock records\n\n" + str(stocks)
        finally:
            await client.close()

    except Exception as e:
        logger.error(f"Error fetching stock levels for {client_name}: {str(e)}")
        return f"Error: {str(e)}"


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run()
