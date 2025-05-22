import heapq
from datetime import datetime, timedelta

# Estructuras de datos
patients = {}  # Diccionario: ID -> {name, contact}
doctors = {}   # Diccionario: ID -> {name, specialty, available_slots}
appointments = []  # Lista: [(datetime, patient_id, doctor_id, priority, urgent)]
urgent_queue = []  # Cola de prioridad: [(priority, datetime, patient_id, doctor_id)]

def add_patient(patient_id, name, contact):
    patients[patient_id] = {"name": name, "contact": contact}
    print(f"Paciente {name} registrado con ID {patient_id}")

def add_doctor(doctor_id, name, specialty):
    # Conjunto de horarios disponibles (9 AM a 5 PM, intervalos de 30 min)
    available_slots = set([datetime(2025, 5, 22, h, m) for h in range(9, 17) for m in (0, 30)])
    doctors[doctor_id] = {"name": name, "specialty": specialty, "available_slots": available_slots}
    print(f"Médico {name} registrado con ID {doctor_id}")

def schedule_appointment(patient_id, doctor_id, date_str, urgent=False):
    if patient_id not in patients or doctor_id not in doctors:
        print("Paciente o médico no encontrado")
        return
    
    try:
        appt_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Formato de fecha inválido. Use YYYY-MM-DD HH:MM")
        return
    
    if appt_time not in doctors[doctor_id]["available_slots"]:
        print("Horario no disponible")
        return
    
    priority = 1 if urgent else 0  # Mayor prioridad para citas urgentes
    doctors[doctor_id]["available_slots"].remove(appt_time)  # Actualizar disponibilidad
    appointments.append((appt_time, patient_id, doctor_id, priority, urgent))
    heapq.heappush(urgent_queue, (-priority, appt_time, patient_id, doctor_id))
    print(f"Cita programada para {patients[patient_id]['name']} con {doctors[doctor_id]['name']} el {appt_time}")

def cancel_appointment(patient_id, doctor_id, date_str):
    try:
        appt_time = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Formato de fecha inválido. Use YYYY-MM-DD HH:MM")
        return
    
    for appt in appointments:
        if appt[1] == patient_id and appt[2] == doctor_id and appt[0] == appt_time:
            appointments.remove(appt)
            doctors[doctor_id]["available_slots"].add(appt_time)
            print(f"Cita cancelada para {patients[patient_id]['name']} el {appt_time}")
            # Nota: No removemos de urgent_queue para simplicidad, pero en un sistema real se manejaría
            return
    print("Cita no encontrada")

def show_doctor_schedule(doctor_id):
    if doctor_id not in doctors:
        print("Médico no encontrado")
        return
    print(f"\nHorarios disponibles para {doctors[doctor_id]['name']}:")
    for slot in sorted(doctors[doctor_id]["available_slots"]):
        print(slot.strftime("%Y-%m-%d %H:%M"))
    print("\nCitas programadas:")
    for appt in appointments:
        if appt[2] == doctor_id:
            print(f"{appt[0].strftime('%Y-%m-%d %H:%M')} - {patients[appt[1]]['name']} {'(Urgente)' if appt[4] else ''}")

def process_urgent_appointments():
    print("\nProcesando citas urgentes:")
    while urgent_queue:
        priority, appt_time, patient_id, doctor_id = heapq.heappop(urgent_queue)
        print(f"Cita urgente: {patients[patient_id]['name']} con {doctors[doctor_id]['name']} el {appt_time}")
        break  # Procesar solo la más urgente por ahora

# Menú interactivo
def main():
    add_patient("P001", "Juan Pérez", "juan@example.com")
    add_doctor("D001", "Dra. García", "Cardiología")
    
    while True:
        print("\n1. Agregar paciente")
        print("2. Agregar médico")
        print("3. Programar cita")
        print("4. Cancelar cita")
        print("5. Mostrar horario médico")
        print("6. Procesar citas urgentes")
        print("7. Salir")
        choice = input("Seleccione una opción: ")
        
        if choice == "1":
            patient_id = input("ID del paciente: ")
            name = input("Nombre: ")
            contact = input("Contacto: ")
            add_patient(patient_id, name, contact)
        elif choice == "2":
            doctor_id = input("ID del médico: ")
            name = input("Nombre: ")
            specialty = input("Especialidad: ")
            add_doctor(doctor_id, name, specialty)
        elif choice == "3":
            patient_id = input("ID del paciente: ")
            doctor_id = input("ID del médico: ")
            date_str = input("Fecha y hora (YYYY-MM-DD HH:MM): ")
            urgent = input("¿Es urgente? (s/n): ").lower() == "s"
            schedule_appointment(patient_id, doctor_id, date_str, urgent)
        elif choice == "4":
            patient_id = input("ID del paciente: ")
            doctor_id = input("ID del médico: ")
            date_str = input("Fecha y hora (YYYY-MM-DD HH:MM): ")
            cancel_appointment(patient_id, doctor_id, date_str)
        elif choice == "5":
            doctor_id = input("ID del médico: ")
            show_doctor_schedule(doctor_id)
        elif choice == "6":
            process_urgent_appointments()
        elif choice == "7":
            print("Saliendo...")
            break
        else:
            print("Opción inválida")

if __name__ == "__main__":
    main()
