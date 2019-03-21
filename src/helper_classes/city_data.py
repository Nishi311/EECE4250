
class CityData(object):
    def __init__(self, city_name=None, attribute_names=None, attribute_values=None):
        self.city_name = city_name if city_name else ""
        self.attributes = {}

        if attribute_names and attribute_values:
            if len(attribute_names) == len(attribute_values):
                for index, val in enumerate(attribute_names):
                    self.attributes[val] = attribute_values[index]
            else:
                self.exit_with_error("Number of attribute names and number of attribute values given do NOT match")


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
