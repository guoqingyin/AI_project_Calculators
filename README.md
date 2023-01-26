# AI_project_Calculators

This project is realised based on the Library cvzone. https://github.com/cvzone/cvzone

## Chinese number gestures

![28 Chinese Number Gestures Stock Vectors, Images & Vector Art | Shutterstock](https://image.shutterstock.com/image-vector/vector-hand-sign-chinese-number-260nw-56305957.jpg)

## Operators

0: =

1: +

2: -

3: *

4: /

5: (

6: )

7: .

8: del

9: AC

## How to use

You need to install all required libraries of python first.

```python
pip install -r requirements.txt
```

### Generate trainning data

run the dataset_generation.py to generate your own data

```python
python dataset_generation.py -n <number>
```

number denotes the number of the gesture

### Train the data

run the whole train notebook to train your model and evaluate the model

### Test the performance of the model

Run the test_number.py to test the model

### Run the calculator

Run the calculator.py to use the calculator
