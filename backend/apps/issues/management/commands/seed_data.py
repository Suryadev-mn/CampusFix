from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.authentication.models import User
from apps.departments.models import Department, Building, Classroom
from apps.issues.models import Issue, StatusHistory, Comment, Upvote
from apps.notifications.models import Notification

class Command(BaseCommand):
    help = 'Seeds the database with test users, departments, classrooms, and realistic campus issues.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE('Starting CampusFix database seeding...'))

        # 1. Create Departments (Facility + Academic)
        departments_data = [
            # Facility & Maintenance Departments (for Staff / Technicians)
            {'name': 'Electrical & Power Systems', 'code': 'ELEC', 'category': 'facility', 'description': 'Maintenance of electrical wiring, sockets, lights, and air conditioning.'},
            {'name': 'Plumbing & Water Facilities', 'code': 'PLUMB', 'category': 'facility', 'description': 'Management of water supply, washrooms, leaks, and drainage systems.'},
            {'name': 'IT & Campus Network', 'code': 'ITNET', 'category': 'facility', 'description': 'Campus Wi-Fi routers, projectors, lab PCs, and network switches.'},
            {'name': 'Civil & Furniture Works', 'code': 'CIVIL', 'category': 'facility', 'description': 'Desks, chairs, doors, windows, paint, and masonry repairs.'},
            {'name': 'Housekeeping & Sanitation', 'code': 'CLEAN', 'category': 'facility', 'description': 'Campus cleanliness, waste disposal, floor scrubbing, and hygiene.'},
            {'name': 'Laboratory Safety & Equipment', 'code': 'LAB', 'category': 'facility', 'description': 'Chemical hoods, emergency eyewashes, lab equipment safety.'},

            # Academic Departments / Engineering Branches (for Students)
            {'name': 'Computer Science & Engineering', 'code': 'CSE', 'category': 'academic', 'description': 'Undergraduate and postgraduate computer science engineering.'},
            {'name': 'Information Science & Engineering', 'code': 'ISE', 'category': 'academic', 'description': 'Information systems, software development, and cloud computing.'},
            {'name': 'Electronics & Communication Engineering', 'code': 'ECE', 'category': 'academic', 'description': 'Embedded systems, signal processing, and communication networks.'},
            {'name': 'Electrical & Electronics Engineering', 'code': 'EEE', 'category': 'academic', 'description': 'Power systems, electronics, control systems, and renewable energy.'},
            {'name': 'Artificial Intelligence & Machine Learning', 'code': 'AIML', 'category': 'academic', 'description': 'Deep learning, computer vision, NLP, and intelligent data systems.'},
            {'name': 'Computer Science & Business Systems', 'code': 'CSBS', 'category': 'academic', 'description': 'Interdisciplinary program in computing and enterprise business systems.'},
            {'name': 'Mechanical Engineering', 'code': 'MECH', 'category': 'academic', 'description': 'Thermodynamics, robotics, manufacturing, and mechanics.'},
            {'name': 'Civil Engineering', 'code': 'CIVIL_ENG', 'category': 'academic', 'description': 'Structural design, construction technology, and environmental engineering.'},
        ]

        departments = {}
        for d in departments_data:
            dept, _ = Department.objects.get_or_create(code=d['code'], defaults=d)
            if dept.category != d.get('category', 'facility'):
                dept.category = d.get('category', 'facility')
                dept.save(update_fields=['category'])
            departments[d['code']] = dept

        self.stdout.write(self.style.SUCCESS(f'Created {len(departments)} departments (Academic + Facility).'))

        # 2. Create Buildings
        buildings_data = [
            {'name': 'Aryabhata Academic Block', 'code': 'AAB', 'total_floors': 4, 'description': 'Main lecture halls and administrative offices.'},
            {'name': 'Alan Turing Computer Center', 'code': 'TCC', 'total_floors': 5, 'description': 'Computer science labs, server rooms, and faculty offices.'},
            {'name': 'Ramanujan Science Wing', 'code': 'RSW', 'total_floors': 3, 'description': 'Physics, Chemistry, and Biotech laboratories.'},
            {'name': 'Central Knowledge Library', 'code': 'CKL', 'total_floors': 4, 'description': 'Study halls, digital archives, and quiet reading zones.'},
            {'name': 'Kalam Student Center', 'code': 'KSC', 'total_floors': 2, 'description': 'Cafeteria, recreation rooms, and student council chambers.'},
        ]

        buildings = {}
        for b in buildings_data:
            bldg, _ = Building.objects.get_or_create(code=b['code'], defaults=b)
            buildings[b['code']] = bldg

        self.stdout.write(self.style.SUCCESS(f'Created {len(buildings)} buildings.'))

        # 3. Create Classrooms
        classrooms_data = [
            {'building': buildings['AAB'], 'room_number': '101', 'floor': 1},
            {'building': buildings['AAB'], 'room_number': '204', 'floor': 2},
            {'building': buildings['AAB'], 'room_number': 'Audi-A', 'floor': 1},
            {'building': buildings['TCC'], 'room_number': 'CS-Lab-301', 'floor': 3},
            {'building': buildings['TCC'], 'room_number': 'IoT-Lab-202', 'floor': 2},
            {'building': buildings['RSW'], 'room_number': 'Chem-Lab-1', 'floor': 1},
            {'building': buildings['RSW'], 'room_number': 'Physics-Lab-2', 'floor': 2},
            {'building': buildings['CKL'], 'room_number': 'Quiet-Hall-3B', 'floor': 3},
            {'building': buildings['CKL'], 'room_number': 'Conference-4', 'floor': 4},
        ]

        classrooms = []
        for c in classrooms_data:
            room, _ = Classroom.objects.get_or_create(
                building=c['building'],
                room_number=c['room_number'],
                defaults={'floor': c['floor']}
            )
            classrooms.append(room)

        self.stdout.write(self.style.SUCCESS(f'Created {len(classrooms)} classrooms with QR codes.'))

        # 4. Create Users
        # Admin
        admin_user, _ = User.objects.get_or_create(
            email='admin@campusfix.edu',
            defaults={
                'username': 'admin',
                'first_name': 'Campus',
                'last_name': 'Administrator',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+1 (555) 019-2831',
                'identifier': 'ADM-001'
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()

        # Staff
        staff_data = [
            {'email': 'electrician@campusfix.edu', 'username': 'rajesh_elec', 'first_name': 'Rajesh', 'last_name': 'Kumar', 'role': 'staff', 'dept': 'ELEC', 'id': 'STF-E01', 'phone': '+1 555 101'},
            {'email': 'network@campusfix.edu', 'username': 'amit_net', 'first_name': 'Amit', 'last_name': 'Sharma', 'role': 'staff', 'dept': 'ITNET', 'id': 'STF-N02', 'phone': '+1 555 102'},
            {'email': 'plumber@campusfix.edu', 'username': 'suresh_plumb', 'first_name': 'Suresh', 'last_name': 'Patel', 'role': 'staff', 'dept': 'PLUMB', 'id': 'STF-P03', 'phone': '+1 555 103'},
            {'email': 'cleaner@campusfix.edu', 'username': 'manoj_clean', 'first_name': 'Manoj', 'last_name': 'Singh', 'role': 'staff', 'dept': 'CLEAN', 'id': 'STF-C04', 'phone': '+1 555 104'},
            {'email': 'carpenter@campusfix.edu', 'username': 'vikram_civil', 'first_name': 'Vikram', 'last_name': 'Rathore', 'role': 'staff', 'dept': 'CIVIL', 'id': 'STF-C05', 'phone': '+1 555 105'},
            {'email': 'labtech@campusfix.edu', 'username': 'priya_lab', 'first_name': 'Priya', 'last_name': 'Nair', 'role': 'staff', 'dept': 'LAB', 'id': 'STF-L06', 'phone': '+1 555 106'},
        ]

        staff_users = {}
        for s in staff_data:
            stf, _ = User.objects.get_or_create(
                email=s['email'],
                defaults={
                    'username': s['username'],
                    'first_name': s['first_name'],
                    'last_name': s['last_name'],
                    'role': s['role'],
                    'department': departments[s['dept']],
                    'identifier': s['id'],
                    'phone': s['phone'],
                    'is_staff': True,
                }
            )
            stf.set_password('staff123')
            stf.save()
            staff_users[s['dept']] = stf

        # Students
        students_data = [
            {'email': 'student@campusfix.edu', 'username': 'aarav_g', 'first_name': 'Aarav', 'last_name': 'Gupta', 'id': 'CS-2023-042', 'phone': '+1 555 201', 'dept': 'CSE'},
            {'email': 'sarah@campusfix.edu', 'username': 'sarah_j', 'first_name': 'Sarah', 'last_name': 'Jenkins', 'id': 'EC-2024-118', 'phone': '+1 555 202', 'dept': 'ECE'},
            {'email': 'rohan@campusfix.edu', 'username': 'rohan_v', 'first_name': 'Rohan', 'last_name': 'Verma', 'id': 'ME-2023-089', 'phone': '+1 555 203', 'dept': 'MECH'},
        ]

        students = []
        for st in students_data:
            stud, _ = User.objects.get_or_create(
                email=st['email'],
                defaults={
                    'username': st['username'],
                    'first_name': st['first_name'],
                    'last_name': st['last_name'],
                    'role': 'student',
                    'identifier': st['id'],
                    'phone': st['phone'],
                    'department': departments.get(st['dept']),
                }
            )
            stud.set_password('student123')
            stud.department = departments.get(st['dept'])
            stud.save()
            students.append(stud)

        self.stdout.write(self.style.SUCCESS('Created Admin, Staff, and Student users.'))

        # 5. Create Sample Issues
        now = timezone.now()
        issues_data = [
            {
                'title': 'High-Definition Projector HDMI Port Damaged',
                'description': 'The HDMI port on the ceiling projector is loose and colors are tinting pink and flickering during lectures. Faculty unable to deliver slides.',
                'category': 'Electrical',
                'status': 'In Progress',
                'priority': 'High',
                'student': students[0],
                'assigned_to': staff_users['ELEC'],
                'department': departments['ELEC'],
                'building': buildings['TCC'],
                'classroom': classrooms[3], # CS-Lab-301
                'location_detail': 'Lectern podium front wall',
                'repair_notes': 'Ordered replacement HDMI wall faceplate. Technicians currently rewiring video splitter.',
                'created_at': now - timedelta(days=2, hours=4),
            },
            {
                'title': 'Ceiling AC Unit Dripping Water Directly onto Student Desks',
                'description': 'Water condensation is leaking heavily from the right split AC cassette. Several notebooks got soaked this morning.',
                'category': 'Electrical',
                'status': 'Assigned',
                'priority': 'Urgent',
                'student': students[1],
                'assigned_to': staff_users['ELEC'],
                'department': departments['ELEC'],
                'building': buildings['AAB'],
                'classroom': classrooms[1], # Room 204
                'location_detail': 'Row 3 right corner near window',
                'created_at': now - timedelta(days=1, hours=2),
            },
            {
                'title': 'High-Density Wi-Fi Access Point Dropping Connections',
                'description': 'The Cisco AP in the quiet study area repeatedly drops Wi-Fi signals every 3-5 minutes with DNS lookup failure.',
                'category': 'Wi-Fi',
                'status': 'Pending',
                'priority': 'Urgent',
                'student': students[0],
                'assigned_to': None,
                'department': departments['ITNET'],
                'building': buildings['CKL'],
                'classroom': classrooms[7], # Quiet-Hall-3B
                'location_detail': 'Ceiling mount near Section C book stacks',
                'created_at': now - timedelta(hours=6),
            },
            {
                'title': 'Broken Wooden Lecture Bench with Sharp Exposed Screws',
                'description': 'The bench on row 4 has cracked wood and two protruding screws that tore a student backpack.',
                'category': 'Furniture',
                'status': 'Resolved',
                'priority': 'Medium',
                'student': students[2],
                'assigned_to': staff_users['CIVIL'],
                'department': departments['CIVIL'],
                'building': buildings['AAB'],
                'classroom': classrooms[0], # Room 101
                'location_detail': 'Row 4, seat 6',
                'repair_notes': 'Reinforced wooden frame with industrial brackets and counter-sunk flush screws. Sanded and revarnished.',
                'resolved_at': now - timedelta(hours=8),
                'created_at': now - timedelta(days=4),
            },
            {
                'title': 'Fume Hood Ventilation Motor Stalled - Safety Hazard',
                'description': 'Exhaust fan in organic synthesis chamber not drawing air. Chemical vapors accumulating during practical labs.',
                'category': 'Safety',
                'status': 'In Progress',
                'priority': 'Urgent',
                'student': students[1],
                'assigned_to': staff_users['LAB'],
                'department': departments['LAB'],
                'building': buildings['RSW'],
                'classroom': classrooms[5], # Chem-Lab-1
                'location_detail': 'Fume Hood Station #3',
                'repair_notes': 'Motor capacitor burnt out. Sourced replacement unit from central inventory. Safety barrier tape installed.',
                'created_at': now - timedelta(days=1, hours=10),
            },
            {
                'title': 'Washroom Flush Valve Stuck Running Continuously',
                'description': 'Third floor men washroom flush valve is stuck open causing significant water wastage and floor overflow.',
                'category': 'Plumbing',
                'status': 'Resolved',
                'priority': 'Medium',
                'student': students[2],
                'assigned_to': staff_users['PLUMB'],
                'department': departments['PLUMB'],
                'building': buildings['AAB'],
                'classroom': classrooms[1],
                'location_detail': 'Restroom 3rd floor west wing',
                'repair_notes': 'Replaced diaphragm valve and reset water pressure regulator.',
                'resolved_at': now - timedelta(days=1),
                'created_at': now - timedelta(days=3),
            },
            {
                'title': 'Conference Room Presentation Display Flickering',
                'description': '85-inch digital signage TV keeps power cycling when HDMI 2 input is selected.',
                'category': 'Electrical',
                'status': 'Closed',
                'priority': 'Low',
                'student': students[0],
                'assigned_to': staff_users['ELEC'],
                'department': departments['ELEC'],
                'building': buildings['CKL'],
                'classroom': classrooms[8],
                'location_detail': 'Boardroom conference wall',
                'repair_notes': 'Replaced surge protector and upgraded firmware.',
                'resolved_at': now - timedelta(days=5),
                'created_at': now - timedelta(days=8),
            }
        ]

        created_issues = []
        for data in issues_data:
            created_time = data.pop('created_at')
            issue = Issue.objects.create(**data)
            # update timestamps explicitly
            Issue.objects.filter(id=issue.id).update(created_at=created_time)
            issue.refresh_from_db()
            issue.calculate_priority_score()
            issue.save()
            created_issues.append(issue)

            # Create status history
            StatusHistory.objects.create(
                issue=issue,
                status='Pending',
                changed_by=issue.student,
                notes='Issue originally reported via CampusFix portal'
            )
            if issue.status != 'Pending':
                StatusHistory.objects.create(
                    issue=issue,
                    status=issue.status,
                    changed_by=issue.assigned_to or admin_user,
                    notes=issue.repair_notes or f'Status updated to {issue.status}'
                )

        self.stdout.write(self.style.SUCCESS(f'Created {len(created_issues)} sample complaints.'))

        # 6. Add Upvotes
        for i, issue in enumerate(created_issues):
            for student in students[:(i % 3) + 1]:
                Upvote.objects.get_or_create(issue=issue, user=student)
            issue.calculate_priority_score()
            issue.save()

        # 7. Add Comments
        Comment.objects.create(
            issue=created_issues[0],
            author=students[0],
            content="Professor had to postpone the guest presentation because of this today. Really urgent!"
        )
        Comment.objects.create(
            issue=created_issues[0],
            author=staff_users['ELEC'],
            content="We have obtained the HDMI switch module. Installing tomorrow morning before 9 AM classes."
        )
        Comment.objects.create(
            issue=created_issues[1],
            author=staff_users['ELEC'],
            content="AC technician team dispatched. Please keep desks clear under the cassette."
        )

        # 8. Add Notifications
        Notification.objects.create(
            recipient=students[0],
            title="Issue #1 Status Updated",
            message="Your report 'High-Definition Projector HDMI Port Damaged' is now In Progress.",
            notification_type='status_change',
            issue=created_issues[0]
        )
        Notification.objects.create(
            recipient=students[1],
            title="New Comment on Your Issue",
            message="Rajesh Kumar commented on your AC leak report.",
            notification_type='comment',
            issue=created_issues[1]
        )

        self.stdout.write(self.style.SUCCESS('Database seeding finished successfully!'))
        self.stdout.write(self.style.NOTICE(
            "\nTest Accounts:\n"
            "  Admin:   admin@campusfix.edu     / admin123\n"
            "  Staff:   electrician@campusfix.edu / staff123 (Electrical)\n"
            "           network@campusfix.edu   / staff123 (IT & Wi-Fi)\n"
            "           plumber@campusfix.edu   / staff123 (Plumbing)\n"
            "  Student: student@campusfix.edu   / student123\n"
            "           sarah@campusfix.edu     / student123\n"
        ))
