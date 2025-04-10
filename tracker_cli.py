import argparse
from datetime import datetime
from sqlalchemy import func, extract
from database import get_db_session
from models import Expense, Budget

def add_expense(args):
    session = get_db_session()
    expense = Expense(
        amount=args.amount,
        category=args.category,
        date=datetime.strptime(args.date, "%Y-%m-%d").date(),
        description=args.description
    )
    session.add(expense)
    session.commit()
    check_budget_alert(args.category, args.amount, args.date)
    print("Expense added successfully")

def set_budget(args):
    session = get_db_session()
    budget = Budget(
        category=args.category,
        month=args.month,
        year=args.year,
        amount=args.amount
    )
    session.add(budget)
    session.commit()
    print("Budget set successfully")

def check_budget_alert(category, amount, date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    session = get_db_session()
    
    budget = session.query(Budget).filter(
        Budget.category == category,
        Budget.month == date.month,
        Budget.year == date.year
    ).first()
    
    if not budget:
        return
    
    total_spent = session.query(func.sum(Expense.amount)).filter(
        Expense.category == category,
        extract('month', Expense.date) == date.month,
        extract('year', Expense.date) == date.year
    ).scalar() or 0
    
    if total_spent > budget.amount:
        print(f"Alert! Exceeded budget for {category}. Budget: {budget.amount}, Spent: {total_spent}")

def generate_report(args):
    session = get_db_session()
    results = session.query(
        extract('month', Expense.date).label('month'),
        extract('year', Expense.date).label('year'),
        Expense.category,
        func.sum(Expense.amount).label('total')
    ).group_by('month', 'year', 'category').all()
    
    for row in results:
        budget = session.query(Budget).filter(
            Budget.category == row.category,
            Budget.month == row.month,
            Budget.year == row.year
        ).first()
        
        print(f"\n{row.year}-{row.month} | {row.category}")
        print(f"Total Spent: {row.total}")
        print(f"Budget: {budget.amount if budget else 'Not set'}")
        if budget:
            print(f"Remaining: {budget.amount - row.total}")

def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers()

    # Add Expense
    expense_parser = subparsers.add_parser('add-expense')
    expense_parser.add_argument('--amount', type=float, required=True)
    expense_parser.add_argument('--category', required=True)
    expense_parser.add_argument('--date', required=True)
    expense_parser.add_argument('--description')
    expense_parser.set_defaults(func=add_expense)

    # Set Budget
    budget_parser = subparsers.add_parser('set-budget')
    budget_parser.add_argument('--category', required=True)
    budget_parser.add_argument('--month', type=int, required=True)
    budget_parser.add_argument('--year', type=int, required=True)
    budget_parser.add_argument('--amount', type=float, required=True)
    budget_parser.set_defaults(func=set_budget)

    # Generate Report
    report_parser = subparsers.add_parser('generate-report')
    report_parser.set_defaults(func=generate_report)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()