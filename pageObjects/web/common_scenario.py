import json


class CommonScenario:
    def __init__(self, page, request):
        self.page = page
        self.request = request
        self.my_map = {}

    def take_screenshot(self, name: str):
        # Placeholder for screenshot attachment logic
        pass

    def hooks(self):
        print("hook from the scenario page")

    def set_value(self, key: str, value: str):
        self.my_map[key] = value

    def get_value(self, key: str):
        return self.my_map.get(key)

    def a11y_analysis(self):
        # Placeholder for accessibility analysis
        pass

    def load_test_data(self, file_path):
        """Load and parse test data from a JSON file.
        
        Args:
            file_path: String path to the JSON file to be loaded.
            
        Returns:
            Parsed JSON data as a dictionary or list.
            
        Raises:
            FileNotFoundError: If the file does not exist at the specified path.
            json.JSONDecodeError: If the file contains invalid JSON format.
        """
        try:
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    return data
                except json.JSONDecodeError as json_error:
                    raise json.JSONDecodeError(
                        f"Invalid JSON format in file: {file_path}. Error: {str(json_error)}",
                        json_error.doc,
                        json_error.pos
                    )
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found at specified path: {file_path}")
