from collections import Counter

# Questions with their associated keyword for mapping
questions = {
    "liking-poem": "Which poem do you like more?",
    "rhyming-poem": "Which poem has better rhyming?",
    "grammatical-poem": "Which poem is more grammatical?",
    "readable-poem": "Which poem is more readable?",
    "melodious-poem": "Which poem is more melodious?",
    "intense-poem": "Which poem is more intense?",
    "coherent-poem": "Which poem is more coherent?",
    "real-poem": "Which poem looks more like a real poem?",
    "comprehensible-poem": "Which poem is more comprehensible?",
    "moved-poem": "Which poem moves you emotionally more?",
}


class PairwisePoems:
    """ Serialization class to store up to 4 questions with two poems assigned to their datasets"""
    def __init__(self, pair_id, poem1, poem2, dataset1, dataset2,
                 question1, question1_id,
                 question2, question2_id,
                 question3, question3_id,
                 question4="", question4_id=""):
        super().__init__()
        self.pair_id = pair_id
        self.poem1 = poem1.strip()
        self.poem2 = poem2.strip()
        self.poem1_dataset = dataset1
        self.poem2_dataset = dataset2
        self.question1 = question1
        self.question1_id = question1_id
        self.question2 = question2
        self.question2_id = question2_id
        self.question3 = question3
        self.question3_id = question3_id
        self.question4 = question4
        self.question4_id = question4_id

    def __eq__(self, other):
        if self.poem1 != other.poem1:
            return False
        if self.poem2 != other.poem2:
            return False
        if self.question1_id != other.question1_id:
            return False
        if self.question2_id != other.question2_id:
            return False
        if self.question3_id != other.question3_id:
            return False
        if self.question4_id != other.question4_id:
            return False
        return True


class DatasetEntry:
    """ Whole pairwise annotated entry with the various categories """
    def __init__(self, id, poem1, poem2, dataset1, dataset2):
        self.id = id
        self.poem1 = poem1
        self.poem2 = poem2
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.coherent = []
        self.grammatical = []
        self.melodious = []
        self.moved = []
        self.real = []
        self.rhyming = []
        self.readable = []
        self.comprehensible = []
        self.intense = []
        self.liking = []

    def update_values(self, values):
        """
        Adds values based on their associated key:
        :param values   dictionary with keys named same the categories or with -poem appended holding lists
                        of values to be appended to the respective categories

        """
        for key in values:
            attribute = key.replace("-poem", "")
            attribute = str(attribute)
            # Find the true attribute
            attribute_values = values[key]
            attribute_value = ""
            for key in attribute_values.keys():
                if attribute_values[key]:
                    attribute_value = key
            current_list = getattr(self, attribute)
            if (len(current_list) >= 3):
                continue
                
            current_list.append(attribute_value)
            setattr(self, attribute, current_list)

    def get_consensus(self):
        """ Reduces the lists of 3 votes in each category for a pair by taking the majority of votes"""
        consensus_obj = DatasetEntry(self.id, self.poem1, self.poem2, self.dataset1, self.dataset2)
        att_names = ["coherent", "grammatical", "moved", "real", "rhyming", "readable", "comprehensible", "intense",
                     "liking"]
        for att_name in att_names:
            att = getattr(self, att_name)
            votes = Counter(att).most_common(3)
            # Check if votes are equally
            if len(votes) > 1 and votes[0][1] == votes[1][1] and votes[1][1] == votes[2][1]:
                vote = "na"
            else:
                vote = votes[0][0]
            setattr(consensus_obj, att_name, vote)
        return consensus_obj

    def __str__(self):
        return str(self.__dict__)

class PairwisePoemsExt:
    """ Serialization class for the dataset extension with 5 instead of 3-4 questions """
    def __init__(self, pair_id, poem1, poem2, dataset1, dataset2,
                 question1, question1_id,
                 question2, question2_id,
                 question3, question3_id,
                 question4, question4_id,
                 question5, question5_id):
        super().__init__()
        self.pair_id = pair_id
        self.poem1 = poem1.strip()
        self.poem2 = poem2.strip()
        self.poem1_dataset = dataset1
        self.poem2_dataset = dataset2
        self.question1 = question1
        self.question1_id = question1_id
        self.question2 = question2
        self.question2_id = question2_id
        self.question3 = question3
        self.question3_id = question3_id
        self.question4 = question4
        self.question4_id = question4_id
        self.question5 = question5
        self.question5_id = question5_id

    def __eq__(self, other):
        if self.poem1 != other.poem1:
            return False
        if self.poem2 != other.poem2:
            return False
        if self.question1_id != other.question1_id:
            return False
        if self.question2_id != other.question2_id:
            return False
        if self.question3_id != other.question3_id:
            return False
        if self.question4_id != other.question4_id:
            return False
        if self.question5_id != other.question5_id:
            return False
        return True
