from helpdesk.models import Customer, Tag, Ticket, Comment

print("Limpiando datos previos de la sesión 2...")

Comment.objects.all().delete()
Ticket.objects.all().delete()
Tag.objects.all().delete()
Customer.objects.all().delete()

print("Creando clientes...")

customer_1 = Customer.objects.create(
    name="ACME Corp",
    email="soporte@acme.com",
    company="ACME",
)

customer_2 = Customer.objects.create(
    name="Globex",
    email="it@globex.com",
    company="Globex Corporation",
)

customer_3 = Customer.objects.create(
    name="Initech",
    email="help@initech.com",
    company="Initech",
)

print("Creando tags...")

tag_login = Tag.objects.create(name="Login", slug="login")
tag_billing = Tag.objects.create(name="Billing", slug="billing")
tag_urgent = Tag.objects.create(name="Urgent", slug="urgent")
tag_support = Tag.objects.create(name="Support", slug="support")

print("Creando tickets...")

ticket_1 = Ticket.objects.create(
    title="No se puede iniciar sesión en el portal",
    description="Varios usuarios reportan error al autenticarse en la plataforma principal.",
    customer=customer_1,
    status=Ticket.Status.OPEN,
    priority=Ticket.Priority.HIGH,
)

ticket_2 = Ticket.objects.create(
    title="Factura generada con valor incorrecto",
    description="El valor cobrado no coincide con el plan contratado por el cliente.",
    customer=customer_2,
    status=Ticket.Status.IN_PROGRESS,
    priority=Ticket.Priority.MEDIUM,
)

ticket_3 = Ticket.objects.create(
    title="Consulta sobre cambio de contraseña",
    description="El cliente desea conocer la política de rotación de contraseñas.",
    customer=customer_1,
    status=Ticket.Status.CLOSED,
    priority=Ticket.Priority.LOW,
)

ticket_4 = Ticket.objects.create(
    title="Error al descargar reporte mensual",
    description="El sistema muestra error 500 al generar el reporte PDF.",
    customer=customer_3,
    status=Ticket.Status.OPEN,
    priority=Ticket.Priority.HIGH,
)

ticket_5 = Ticket.objects.create(
    title="Intermitencia en módulo de soporte",
    description="El módulo tarda demasiado en cargar durante ciertos momentos del día.",
    customer=customer_2,
    status=Ticket.Status.OPEN,
    priority=Ticket.Priority.MEDIUM,
)

print("Asociando tags...")

ticket_1.tags.add(tag_login, tag_urgent, tag_support)
ticket_2.tags.add(tag_billing, tag_support)
ticket_3.tags.add(tag_login)
ticket_4.tags.add(tag_urgent, tag_support)
ticket_5.tags.add(tag_support)

print("Creando comentarios...")

Comment.objects.create(
    ticket=ticket_1,
    author_name="Mesa de ayuda",
    body="Se solicita captura del error presentado por el usuario.",
)

Comment.objects.create(
    ticket=ticket_1,
    author_name="Cliente",
    body="Se adjunta evidencia del mensaje mostrado en pantalla.",
)

Comment.objects.create(
    ticket=ticket_2,
    author_name="Agente de facturación",
    body="Se valida inconsistencia en el cálculo del impuesto.",
)

Comment.objects.create(
    ticket=ticket_2,
    author_name="Supervisor",
    body="Se escala el caso al equipo financiero para revisión adicional.",
    is_internal=True,
)

Comment.objects.create(
    ticket=ticket_4,
    author_name="Mesa de ayuda",
    body="Se reproduce el error al generar el reporte en ambiente local.",
)

Comment.objects.create(
    ticket=ticket_5,
    author_name="Operaciones",
    body="Se detecta degradación del rendimiento en horas pico.",
    is_internal=True,
)

print("Carga completada correctamente.")
print(f"Clientes: {Customer.objects.count()}")
print(f"Tags: {Tag.objects.count()}")
print(f"Tickets: {Ticket.objects.count()}")
print(f"Comentarios: {Comment.objects.count()}")
