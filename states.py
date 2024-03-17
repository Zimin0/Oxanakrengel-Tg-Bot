from aiogram.fsm.state import StatesGroup, State

class OrderClothes(StatesGroup):
    show_clothes = State()
    choose_size = State()
    choose_payment_method = State()
    get_personal_data = State()
    choose_delivery_method = State() 
    send_request_to_support = State()

class PersonalDataForm(StatesGroup):
    wait_for_name = State()
    wait_for_surname = State()
    wait_for_email = State()
    wait_for_phone_number = State()
    wait_for_delivery_address = State()

class SupportForm(StatesGroup):
    wait_for_message = State()
    wait_for_confirmation = State()