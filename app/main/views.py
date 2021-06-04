from . import main

@main.route('/home', methods=['GET', 'POST'])
def home():

    return 'hola mundo'