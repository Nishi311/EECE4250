
class CityData(object):
    def __init__(self):
        self.city_name = ""
        self.attributes = []

    def retrieve_all_city_data(self):
        return self.attributes

    def return_attribute_data(self, attribute_name):
        if attribute_name in self.attributes:
            return True, self.attributes[attribute_name]
        else:
            print("Cannot find Attribute {0}. Returning False".format(attribute_name))
            return False, None
