# Import necessary libraries streamlit and simpleai
import streamlit as st
from simpleai.search import CspProblem, backtrack

# Set the page title and icon
st.set_page_config(
    page_title="Cryptoarithmetic Puzzle Solver",
    page_icon="✨",
)

# Define containers to place certain part of the streamlit app in a specified container
header = st.container()
explanation = st.container()
possible_tests = st.container()
result = st.container()

# header contains a welcome to the app
with header:
    st.markdown('<h1 class="blue-title">Cryptoarithmetic Puzzle</h1>', unsafe_allow_html=True)
    st.markdown('<p class="center">Welcome to my awesome first AI task where I code a GUI for a Cryptoarithmetic Puzzle! :)✨</p>', unsafe_allow_html=True)

# explanation contains an explanation of what a cryptoarithmetic puzzle is
with explanation:
    st.markdown('<h3 class="blue-text">What is a cryptoarithmetic puzzle?</h3>', unsafe_allow_html=True)
    st.markdown('<p class="blue-background">A cryptoarithmetic puzzle is a type of word puzzle where letters or symbols represent digits, and the goal is to find the numerical values that correspond to each letter or symbol to make a valid mathematical equation.</p>', unsafe_allow_html=True)

# Defining the example cryptoarithmetic puzzles
puzzles = [
    """
    SEND + MORE = MONEY
    """,
    """
    TWO * TWO = FOUR
    """,
    """
    COCA + COLA = SODA
    """,
    """
    FIVE * FOUR = TWENTY
    """
]

# possible test displays valid examples that the user can test out
with possible_tests:
    st.markdown('<p class="blue-background">Here are some possible puzzlesyou can try out:</p>', unsafe_allow_html=True)
    for puzzle in puzzles:
        st.text(puzzle)

# Define custom CSS style for red text
st.markdown(
    """
    <style>
    .center{
        text-align:center;
    }
    .blue-title {
        color: darkblue;
        text-align: center;
    }
    .blue-text {
        color: darkblue;
    }
    .blue-background {
        background-color: AliceBlue;
        padding: 15px;
        border-radius: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Get input words from the user as well as the desired mathematical operation
word_1 = st.text_input("Enter first word: ").upper()
word_2 = st.text_input("Enter second word: ").upper()
operator = st.selectbox("Select operator:", ["+", "-", "*", "/"])
word_3 = st.text_input("Enter resulting word: ").upper()

# When clicking on the button "Solve" the following code will be triggered
if st.button("Solve"):
    # Convert input words to uppercase and create tuples
    tuple_1 = tuple(word_1)
    tuple_2 = tuple(word_2)
    tuple_3 = tuple(word_3)

    # Define the domains for the first letter of each word
    domains = {
        tuple_1[0]: list(range(1, 10)),
        tuple_2[0]: list(range(1, 10)),
        tuple_3[0]: list(range(1, 10)),
    }

    # Create a tuple containing all letters from the input words
    result_tuple = tuple_1 + tuple_2 + tuple_3

    # Create a set of capitalized letters from the result_tuple
    capitalized_set = set(letter for letter in result_tuple)

    # Extract the first letters of the input words and remove duplicates
    first_letters = list(dict.fromkeys([word_1[0].upper(), word_2[0].upper(), word_3[0].upper()]))

    # Remove the first letters from the capitalized_set
    for first_letter in first_letters:
        if first_letter in capitalized_set:
            capitalized_set.remove(first_letter)

    # Define variables as a tuple of first letters and sorted remaining letters
    variables = tuple(first_letters + sorted(capitalized_set))

    # Define domains for the remaining letters (not the first letter)
    for letter in sorted(capitalized_set):
        domains[letter] = list(range(0, 10))

    # Initialize a list to store index lists for each input word
    index_lists = []
    words = [word_1, word_2, word_3]

    # Create index lists for each word
    for word in words:
        index_list = []  # Create a new index list for each word
        for letter in word:
            if letter.upper() in domains:
                index = list(domains).index(letter.upper())
                index_list.append(index)
        index_lists.append(index_list)  # Append the index list for the current word to the list of index lists

    # Define a constraint function to ensure unique values for variables
    def constraint_unique(variables, values):
        return len(values) == len(set(values))
    
    # Define a constraint function for performing an arithmetic operation
    def constraint_operation(variables, values):
    # Initialize an empty list to store the intermediate results of the operation
        result_list = []

        # Iterate through the list of index lists (one for each input word)
        for index_list in index_lists:
            # Initialize a factor to accumulate the product or sum of digit values
            factor = int("".join(str(values[i]) for i in index_list))
            
            # Append the factor to the result_list
            result_list.append(factor)

        # Check if the operation constraint is satisfied (addition, subtraction, multiplication, division)
        # This constraint checks if the sum or product or subtraction or division of the intermediate factors is equal to the result
        # of the arithmetic operation specified by the puzzle (e.g., WORD_1 + WORD_2 = WORD_3)
        if operator == "+":
            return (result_list[0] + result_list[1]) == result_list[2]
        elif operator == "-":
            return (result_list[0] - result_list[1]) == result_list[2]
        elif operator == "*":
            return (result_list[0] * result_list[1]) == result_list[2]
        elif operator == "/":
            return (result_list[0] / result_list[1]) == result_list[2] if result_list[1] != 0 else False

    # Define constraints as a list of unique and addition constraints
    constraints = [
        (variables, constraint_unique),
        (variables, constraint_operation),
    ]

    # Create a CSP problem with variables, domains, and constraints
    problem = CspProblem(variables, domains, constraints)

    # Use backtrack search to find a solution
    output = backtrack(problem)
    
    # the result container is where we'll show the solution to their inputs
    with result:
        # Set a header for the results section
        st.header('Solutions')
        
        # Check if a solution was found
        if output is not None:
            # Get the value of each letter and store them in a dictionary
            letter_values = {var: value for var, value in output.items()}
            
            # Create a string containing the values of letters in sorted order
            values_row = " ".join(str(letter_values[var]) for var in sorted(letter_values.keys()))
            
            # Create a string of dashes with the length of the longest word
            string = "-" * max(len(word_1), len(word_2), len(word_3))
            
            # Create strings containing the values of individual letters in the input words
            values_word_1 = ''.join(str(letter_values.get(letter, '')) for letter in word_1)
            values_word_2 = ''.join(str(letter_values.get(letter, '')) for letter in word_2)
            values_word_3 = ''.join(str(letter_values.get(letter, '')) for letter in word_3)
            
            # Divide the display into three columns for better layout
            cols = st.columns(3)
            
            # Display letters and their values in the first column
            cols[0].text(f"{' '.join(sorted(letter_values.keys()))}\n{values_row}")
            
            # Display the arithmetic equation in letters in the second column
            cols[1].text(f"{word_1}\n{word_2}  {operator}\n{string}\n{word_3}")
            
            # Display the arithmetic equation in numbers in the third column (technically the solution)
            cols[2].text(f"{values_word_1}\n{values_word_2}  {operator}\n{string}\n{values_word_3}")
        else:
            # If no solution was found, display a message
            st.write("No solution found.")

