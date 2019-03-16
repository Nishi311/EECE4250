
class CityData(object):
    def __init__(self):
        self.city_name = ""
        self.attributes = {}

    def retrieve_all_city_data(self):
        return self.attributes

    def return_attribute_data(self, attribute_name):
        """
        Returns the score the city has for a particular attribute, assuming it HAS that attribute.
        :param attribute_name: The name of the attribute to find.
        :return: tuple (bool, value). bool: True -> Attribute found. Following value will be valid.
                                            False -> Attribute NOT found. Following value will be NONE.
        """
        if attribute_name in self.attributes:
            return True, self.attributes[attribute_name]
        else:
            print("CityData, return_attribute_data(): Cannot find Attribute {0} in object "
                   "{1}.".format(attribute_name, self.city_name))
            return False, None

    @staticmethod
    def exit_with_error(error):
        print("Error. Exiting with message:\n{0}\n".format(error))
        exit(0)
