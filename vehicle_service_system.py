# Vehicle Service Record Management System
# Done by: Vishal

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "service_data.json")


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"vehicles": {}, "services": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def register_vehicle(data):
    number = input("Enter vehicle number: ").strip().upper()
    if not number:
        print("Vehicle number cannot be empty.")
        return
    if number in data["vehicles"]:
        print("Vehicle already registered.")
        return
    data["vehicles"][number] = {
        "owner": input("Enter owner name: ").strip().title(),
        "phone": input("Enter phone number: ").strip(),
        "model": input("Enter vehicle model: ").strip().title(),
    }
    save_data(data)
    print(f"Vehicle {number} registered.")


def view_customers(data):
    print("\n--- Registered Vehicles & Customers ---")
    if not data["vehicles"]:
        print("No vehicles registered.")
        return
    for number, v in data["vehicles"].items():
        print(f"{number} | {v['model']} | Owner: {v['owner']} | Ph: {v['phone']}")


def add_service(data):
    number = input("Enter vehicle number: ").strip().upper()
    if number not in data["vehicles"]:
        print("Vehicle not registered. Please register first.")
        return
    service_type = input("Enter service type (e.g. Oil change, Brake repair): ").strip().title()
    try:
        labour = float(input("Enter labour cost: "))
        parts = float(input("Enter parts cost: "))
    except ValueError:
        print("Invalid cost.")
        return
    km = input("Enter current odometer reading (km): ").strip()
    next_due = input("Next service due date (YYYY-MM-DD, optional): ").strip()

    total = labour + parts
    data["services"].append({
        "number": number,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "service_type": service_type,
        "labour": labour,
        "parts": parts,
        "total": total,
        "km": km,
        "next_due": next_due,
    })
    save_data(data)
    print(f"Service recorded. Total cost: Rs. {total}")


def service_history(data):
    number = input("Enter vehicle number: ").strip().upper()
    if number not in data["vehicles"]:
        print("Vehicle not found.")
        return
    v = data["vehicles"][number]
    print(f"\n--- Service History: {number} ({v['model']}, Owner: {v['owner']}) ---")
    records = [s for s in data["services"] if s["number"] == number]
    if not records:
        print("No service records.")
        return
    for s in records:
        print(f"{s['date']} | {s['service_type']} | {s['km']} km | "
              f"Labour: {s['labour']} | Parts: {s['parts']} | Total: Rs. {s['total']}")
    print(f"Total spent on this vehicle: Rs. {sum(s['total'] for s in records)}")


def upcoming_maintenance(data):
    print("\n--- Upcoming Maintenance ---")
    found = False
    today = datetime.now().strftime("%Y-%m-%d")
    for s in data["services"]:
        if s["next_due"]:
            status = "OVERDUE" if s["next_due"] < today else "Upcoming"
            print(f"{s['number']} | Due: {s['next_due']} | {status}")
            found = True
    if not found:
        print("No maintenance dates recorded.")


def total_income(data):
    total = sum(s["total"] for s in data["services"])
    print(f"\nTotal services done: {len(data['services'])}")
    print(f"Total income: Rs. {total}")


def main():
    data = load_data()
    while True:
        print("\n===== VEHICLE SERVICE RECORD MANAGEMENT =====")
        print("1. Register vehicle / customer")
        print("2. View all customers")
        print("3. Add service record")
        print("4. View service history of a vehicle")
        print("5. Upcoming maintenance")
        print("6. Total service income")
        print("7. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_vehicle(data)
        elif choice == "2":
            view_customers(data)
        elif choice == "3":
            add_service(data)
        elif choice == "4":
            service_history(data)
        elif choice == "5":
            upcoming_maintenance(data)
        elif choice == "6":
            total_income(data)
        elif choice == "7":
            print("Thank you!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == "__main__":
    main()
