#!/usr/bin/env python3
"""
QuickBooks Online MCP Server

A FastMCP-powered Model Context Protocol server for QuickBooks Online API integration
with OAuth 2.0 authentication, following PetesBrain patterns.

Focus: Financial reporting and data queries
"""

from fastmcp import FastMCP, Context
from typing import Any, Dict, List, Optional
import os
import logging
import requests
import json
from datetime import datetime, timedelta

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import OAuth modules
from oauth.quickbooks_auth import get_headers_with_auto_token, get_realm_id

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('quickbooks_server')

# Constants
QB_API_BASE_URL = "https://quickbooks.api.intuit.com/v3/company"
QB_SANDBOX_URL = "https://sandbox-quickbooks.api.intuit.com/v3/company"

# Create FastMCP server
mcp = FastMCP("QuickBooks Reporting Tools")

# Server startup
logger.info("Starting QuickBooks MCP Server...")


def make_api_request(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    method: str = "GET",
    use_sandbox: bool = False
) -> Dict[str, Any]:
    """
    Make a request to QuickBooks Online API with automatic authentication.
    
    Args:
        endpoint: API endpoint (e.g., '/query?query=...')
        params: Query parameters
        method: HTTP method (GET or POST)
        use_sandbox: Whether to use sandbox environment
    
    Returns:
        Dict with API response
    """
    headers = get_headers_with_auto_token()
    realm_id = get_realm_id()
    
    # Build full URL
    base_url = QB_SANDBOX_URL if use_sandbox else QB_API_BASE_URL
    if endpoint.startswith('http'):
        url = endpoint
    else:
        endpoint = endpoint.lstrip('/')
        url = f"{base_url}/{realm_id}/{endpoint}"
    
    logger.info(f"Making {method} request to: {url}")
    
    # Make request
    if method.upper() == "GET":
        response = requests.get(url, params=params, headers=headers)
    elif method.upper() == "POST":
        response = requests.post(url, params=params, headers=headers, json={})
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")
    
    if not response.ok:
        error_msg = f"API request failed: {response.status_code} - {response.text}"
        logger.error(error_msg)
        raise Exception(error_msg)
    
    return response.json()


@mcp.tool()
def get_profit_and_loss(
    start_date: str = None,
    end_date: str = None,
    accounting_method: str = "Accrual",
    summarize_column_by: str = "Total"
) -> Dict[str, Any]:
    """
    Get Profit & Loss (P&L) report from QuickBooks.
    
    Args:
        start_date: Start date in YYYY-MM-DD format (defaults to start of current year)
        end_date: End date in YYYY-MM-DD format (defaults to today)
        accounting_method: "Accrual" or "Cash"
        summarize_column_by: How to summarize - "Total", "Month", "Quarter", "Year"
    
    Returns:
        Dict containing P&L report data
    """
    logger.info(f"Fetching P&L report from {start_date} to {end_date}")
    
    # Set default dates if not provided
    if not start_date:
        start_date = datetime.now().replace(month=1, day=1).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'accounting_method': accounting_method,
        'summarize_column_by': summarize_column_by
    }
    
    try:
        result = make_api_request('reports/ProfitAndLoss', params=params)
        return {
            "success": True,
            "report_name": "Profit & Loss",
            "start_date": start_date,
            "end_date": end_date,
            "accounting_method": accounting_method,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error fetching P&L: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_balance_sheet(
    report_date: str = None,
    accounting_method: str = "Accrual"
) -> Dict[str, Any]:
    """
    Get Balance Sheet report from QuickBooks.
    
    Args:
        report_date: Date for the report in YYYY-MM-DD format (defaults to today)
        accounting_method: "Accrual" or "Cash"
    
    Returns:
        Dict containing Balance Sheet data
    """
    if not report_date:
        report_date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Fetching Balance Sheet as of {report_date}")
    
    params = {
        'date_macro': 'Today' if report_date == datetime.now().strftime('%Y-%m-%d') else None,
        'accounting_method': accounting_method
    }
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        result = make_api_request('reports/BalanceSheet', params=params)
        return {
            "success": True,
            "report_name": "Balance Sheet",
            "report_date": report_date,
            "accounting_method": accounting_method,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error fetching Balance Sheet: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_cash_flow(
    start_date: str = None,
    end_date: str = None,
    accounting_method: str = "Accrual"
) -> Dict[str, Any]:
    """
    Get Cash Flow Statement from QuickBooks.
    
    Args:
        start_date: Start date in YYYY-MM-DD format (defaults to start of current year)
        end_date: End date in YYYY-MM-DD format (defaults to today)
        accounting_method: "Accrual" or "Cash"
    
    Returns:
        Dict containing Cash Flow Statement data
    """
    if not start_date:
        start_date = datetime.now().replace(month=1, day=1).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Fetching Cash Flow from {start_date} to {end_date}")
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'accounting_method': accounting_method
    }
    
    try:
        result = make_api_request('reports/CashFlow', params=params)
        return {
            "success": True,
            "report_name": "Cash Flow",
            "start_date": start_date,
            "end_date": end_date,
            "accounting_method": accounting_method,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error fetching Cash Flow: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_general_ledger(
    start_date: str = None,
    end_date: str = None,
    accounting_method: str = "Accrual"
) -> Dict[str, Any]:
    """
    Get General Ledger report from QuickBooks.
    
    Args:
        start_date: Start date in YYYY-MM-DD format (defaults to start of current month)
        end_date: End date in YYYY-MM-DD format (defaults to today)
        accounting_method: "Accrual" or "Cash"
    
    Returns:
        Dict containing General Ledger data
    """
    if not start_date:
        start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Fetching General Ledger from {start_date} to {end_date}")
    
    params = {
        'start_date': start_date,
        'end_date': end_date,
        'accounting_method': accounting_method
    }
    
    try:
        result = make_api_request('reports/GeneralLedger', params=params)
        return {
            "success": True,
            "report_name": "General Ledger",
            "start_date": start_date,
            "end_date": end_date,
            "accounting_method": accounting_method,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error fetching General Ledger: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_accounts_receivable_aging(
    report_date: str = None,
    aging_method: str = "Current",
    num_periods: int = 4,
    aging_period: int = 30
) -> Dict[str, Any]:
    """
    Get Accounts Receivable Aging report from QuickBooks.
    
    Args:
        report_date: Date for the report in YYYY-MM-DD format (defaults to today)
        aging_method: "Current" or "Report_Date"
        num_periods: Number of aging periods to show
        aging_period: Days in each aging period
    
    Returns:
        Dict containing AR Aging data
    """
    if not report_date:
        report_date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Fetching AR Aging as of {report_date}")
    
    params = {
        'report_date': report_date,
        'aging_method': aging_method,
        'num_periods': num_periods,
        'aging_period': aging_period
    }
    
    try:
        result = make_api_request('reports/AgedReceivables', params=params)
        return {
            "success": True,
            "report_name": "Accounts Receivable Aging",
            "report_date": report_date,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error fetching AR Aging: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_accounts_payable_aging(
    report_date: str = None,
    aging_method: str = "Current",
    num_periods: int = 4,
    aging_period: int = 30
) -> Dict[str, Any]:
    """
    Get Accounts Payable Aging report from QuickBooks.
    
    Args:
        report_date: Date for the report in YYYY-MM-DD format (defaults to today)
        aging_method: "Current" or "Report_Date"
        num_periods: Number of aging periods to show
        aging_period: Days in each aging period
    
    Returns:
        Dict containing AP Aging data
    """
    if not report_date:
        report_date = datetime.now().strftime('%Y-%m-%d')
    
    logger.info(f"Fetching AP Aging as of {report_date}")
    
    params = {
        'report_date': report_date,
        'aging_method': aging_method,
        'num_periods': num_periods,
        'aging_period': aging_period
    }
    
    try:
        result = make_api_request('reports/AgedPayables', params=params)
        return {
            "success": True,
            "report_name": "Accounts Payable Aging",
            "report_date": report_date,
            "data": result
        }
    except Exception as e:
        logger.error(f"Error fetching AP Aging: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def query_accounts(
    account_type: str = None,
    account_name: str = None
) -> Dict[str, Any]:
    """
    Query chart of accounts from QuickBooks.
    
    Args:
        account_type: Filter by account type (e.g., "Bank", "Income", "Expense", "Asset", "Liability", "Equity")
        account_name: Filter by account name (partial match)
    
    Returns:
        Dict containing account data
    """
    logger.info(f"Querying accounts - Type: {account_type}, Name: {account_name}")
    
    # Build SQL query
    query = "SELECT * FROM Account"
    conditions = []
    
    if account_type:
        conditions.append(f"AccountType = '{account_type}'")
    if account_name:
        conditions.append(f"Name LIKE '%{account_name}%'")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " MAXRESULTS 1000"
    
    try:
        result = make_api_request(f'query?query={query}')
        accounts = result.get('QueryResponse', {}).get('Account', [])
        
        return {
            "success": True,
            "count": len(accounts),
            "accounts": accounts
        }
    except Exception as e:
        logger.error(f"Error querying accounts: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def get_company_info() -> Dict[str, Any]:
    """
    Get company information from QuickBooks.
    
    Returns:
        Dict containing company info
    """
    logger.info("Fetching company information")
    
    try:
        realm_id = get_realm_id()
        result = make_api_request(f'companyinfo/{realm_id}')
        
        return {
            "success": True,
            "company_info": result.get('CompanyInfo', {})
        }
    except Exception as e:
        logger.error(f"Error fetching company info: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def query_transactions(
    transaction_type: str,
    start_date: str = None,
    end_date: str = None,
    max_results: int = 100
) -> Dict[str, Any]:
    """
    Query transactions from QuickBooks.
    
    Args:
        transaction_type: Type of transaction (Invoice, Bill, Payment, Purchase, SalesReceipt, etc.)
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        max_results: Maximum number of results (default 100, max 1000)
    
    Returns:
        Dict containing transaction data
    """
    logger.info(f"Querying {transaction_type} transactions")
    
    # Build SQL query
    query = f"SELECT * FROM {transaction_type}"
    conditions = []
    
    if start_date:
        conditions.append(f"TxnDate >= '{start_date}'")
    if end_date:
        conditions.append(f"TxnDate <= '{end_date}'")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += f" MAXRESULTS {min(max_results, 1000)}"
    
    try:
        result = make_api_request(f'query?query={query}')
        transactions = result.get('QueryResponse', {}).get(transaction_type, [])
        
        return {
            "success": True,
            "transaction_type": transaction_type,
            "count": len(transactions),
            "transactions": transactions
        }
    except Exception as e:
        logger.error(f"Error querying transactions: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()

