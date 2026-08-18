from .models import CarMake, CarModel


def initiate():
    if CarModel.objects.exists():
        return

    car_make_data = [
        ("NISSAN", "Great cars. Japanese technology"),
        ("Mercedes", "Great cars. German technology"),
        ("Audi", "Great cars. German technology"),
        ("Kia", "Great cars. Korean technology"),
        ("Toyota", "Great cars. Japanese technology"),
    ]

    makes = {
        name: CarMake.objects.get_or_create(
            name=name,
            defaults={"description": description},
        )[0]
        for name, description in car_make_data
    }

    car_model_data = [
        ("NISSAN", "Pathfinder", "SUV"),
        ("NISSAN", "Qashqai", "SUV"),
        ("NISSAN", "XTRAIL", "SUV"),
        ("Mercedes", "A-Class", "SUV"),
        ("Mercedes", "C-Class", "SUV"),
        ("Mercedes", "E-Class", "SUV"),
        ("Audi", "A4", "SUV"),
        ("Audi", "A5", "SUV"),
        ("Audi", "A6", "SUV"),
        ("Kia", "Sorrento", "SUV"),
        ("Kia", "Carnival", "SUV"),
        ("Kia", "Cerato", "Sedan"),
        ("Toyota", "Corolla", "Sedan"),
        ("Toyota", "Camry", "Sedan"),
        ("Toyota", "Kluger", "SUV"),
    ]

    CarModel.objects.bulk_create(
        [
            CarModel(
                car_make=makes[make_name],
                dealer_id=1,
                name=model_name,
                type=model_type,
                year=2023,
            )
            for make_name, model_name, model_type in car_model_data
        ]
    )
