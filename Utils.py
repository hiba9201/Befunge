class Utils:
    @staticmethod
    def read_file(path):
        try:
            with open(path) as file:
                return file.readlines()
        except OSError:
            return None

    @staticmethod
    def lines_to_table(lines):
        res = []
        if lines is None:
            return []

        max_len = max(list(map(lambda line: len(line), lines)))
        prepared_lines = map(lambda line: line.ljust(max_len), lines)
        for line in prepared_lines:
            res.append(list(line))

        return res

    @staticmethod
    def get_max_len(table):
        return max(list(map(lambda row: len(row), table)))



    @staticmethod
    def sum_lists(list1, list2):
        tmp = zip(list1, list2)
        return map(sum, tmp)
