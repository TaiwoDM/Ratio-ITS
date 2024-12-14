import tkinter as tk
from tkinter import messagebox
from owlready2 import *

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def getData(request):
    response = {
        "quantities": [],
        "steps": [],
        "hints": [],
        "total_value": "N/A",
        "solutions": []
    }

    # Load the ontology
    ontology_path = "api/Ratio.owx" 
    onto = get_ontology(ontology_path).load()

    problem = onto.search_one(iri="*Problem1")
    
    if not problem:
        return None

    if hasattr(problem, 'hasQuantity'):
        for quantity in problem.hasQuantity:
            part = quantity.ratioPart[0] if hasattr(quantity, 'ratioPart') else "N/A"
            response['quantities'].append(part)

    # Get steps and their hints
    if hasattr(problem, 'hasStep'):
        for step in problem.hasStep:
            response['steps'].append(step.description[0])
            response['hints'].append(step.hasHint[0].text[0])
    
    if hasattr(problem, 'hasRatioValue'):
        for ratio_value in problem.hasRatioValue:
            value = ratio_value.calculatedValue[0] if hasattr(ratio_value, 'calculatedValue') else "N/A"
            response['solutions'].append(value)

    response['total_value'] = problem.totalValue[0]

    print(problem)

    return Response(response)