#!/bin/bash

# P9 Budget Deployment Script
# Usage: ./deploy.sh [date]
# Example: ./deploy.sh dec-24

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Base paths
DEPLOYER_PATH="/Users/administrator/Documents/PetesBrain.nosync/tools/universal-budget-deployer"
CSV_PATH="/Users/administrator/Documents/PetesBrain.nosync/clients/smythson/universal-budget-deployer"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to deploy budgets
deploy_budgets() {
    local csv_file=$1
    local description=$2

    print_status "Starting deployment: $description"
    print_status "CSV file: $csv_file"

    # Check if CSV exists
    if [ ! -f "$CSV_PATH/$csv_file" ]; then
        print_error "CSV file not found: $CSV_PATH/$csv_file"
        exit 1
    fi

    # Change to deployer directory
    cd "$DEPLOYER_PATH"

    # Run deployment
    print_status "Deploying budgets..."
    python3 deploy_budgets.py \
        --csv-file "$CSV_PATH/$csv_file" \
        --mode apply \
        --verify

    if [ $? -eq 0 ]; then
        print_status "✅ Deployment successful!"
    else
        print_error "Deployment failed! Check logs."
        exit 1
    fi
}

# Main logic
case "$1" in
    "dec-22")
        deploy_budgets "p9-dec-22-minimal.csv" "Dec 22 - Minimal budgets (£2,000)"
        ;;
    "dec-23")
        deploy_budgets "p9-dec-23-minimal.csv" "Dec 23 - Minimal budgets (£2,000)"
        ;;
    "dec-24")
        print_warning "SALE LAUNCH DAY - Deploy at 17:45 GMT (before 18:00 sale start)!"
        read -p "Are you sure you want to deploy sale launch budgets? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            deploy_budgets "p9-dec-24-6pm-sale-launch.csv" "Dec 24 - Sale Launch (£3,500)"
            print_status "🎄 Sale budgets deployed! Monitor performance closely."
        else
            print_status "Deployment cancelled."
        fi
        ;;
    "dec-25")
        deploy_budgets "p9-dec-25-christmas.csv" "Dec 25 - Christmas Day (£6,000)"
        ;;
    "dec-26")
        print_warning "BOXING DAY - Maximum budget day (£12,000)!"
        read -p "Are you sure you want to deploy Boxing Day maximum budgets? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            deploy_budgets "p9-dec-26-boxing-day.csv" "Dec 26 - Boxing Day Maximum (£12,000)"
            print_status "🎁 Boxing Day budgets deployed! Set up hourly monitoring."
        else
            print_status "Deployment cancelled."
        fi
        ;;
    "dec-27")
        deploy_budgets "p9-dec-27-sustained.csv" "Dec 27 - Sustained High (£10,000)"
        ;;
    "dec-28")
        deploy_budgets "p9-dec-28-final.csv" "Dec 28 - Final P9 Day (£8,000)"
        print_status "🏁 Final P9 budgets deployed!"
        ;;
    "check")
        print_status "Checking current budget status..."
        cd "$DEPLOYER_PATH"
        python3 verify_budgets.py --check-all
        ;;
    *)
        echo "P9 Budget Deployment Script"
        echo "Usage: $0 [date]"
        echo ""
        echo "Available dates:"
        echo "  dec-22  - Deploy Dec 22 minimal budgets (£2,000)"
        echo "  dec-23  - Deploy Dec 23 minimal budgets (£2,000)"
        echo "  dec-24  - Deploy Dec 24 sale launch budgets (£3,500) - RUN AT 17:45!"
        echo "  dec-25  - Deploy Dec 25 Christmas Day budgets (£6,000)"
        echo "  dec-26  - Deploy Dec 26 Boxing Day maximum budgets (£12,000)"
        echo "  dec-27  - Deploy Dec 27 sustained high budgets (£10,000)"
        echo "  dec-28  - Deploy Dec 28 final P9 budgets (£8,000)"
        echo "  check   - Check current budget status"
        echo ""
        echo "Example: $0 dec-24"
        exit 1
        ;;
esac

print_status "Deployment process complete."