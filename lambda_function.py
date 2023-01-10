### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")
    

        ### YOUR DATA VALIDATION CODE STARTS HERE ###
def build_validation_result(is_valid,
violated_slot, message_content):
        """
    Define a result message structured as Lex response.
        """
        if message_content is None:
            return{"isValid": is_valid,
        "violatedSlot": violated_slot,
        "message":{"contentType":
        "PlainText", "content": message_content},
        }
        return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType":
    "PlainText", "content": message_content},
        }
    
    

def validate_data(birthday, dollars, intent_request):
    """
    Validates the data provided by the user.
    """

    # Validate that the user is over 21 years old
    if birthday is not None:
        age = parse_float(age)
        if age < 21:
            return build_validation_result(
                False,
                "birthday",
                "You should be at least 21 years old,and no older than 65 years old, to use this service.",
            )

    # Validate the investment amount, it should be >= 5000
        if dollars is not None:
            dollars = parse_float(
            dollars
        )
            # Since parameters are strings it's important to cast values
        if dollars < 5000:
            return build_validation_result(
                False,
                "dollars",
                "The amount to convert should at least 5000",
                "please provide a correct amount in dollars to convert.",
            )

    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)
    

        ### YOUR DATA VALIDATION CODE ENDS HERE ###

### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return{
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """
    return{
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the initial investment recommendation

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE STARTS HERE ###
    if risk_level == "None":
        initial_recommendation = initial_recomend
    elif risk_level == "Very Low":
        initial_recommendation = "80% bonds (AGG), 20% equities (SPY)"
    elif risk_level == "Low":
        initial_recommendation = "60% bonds (AGG), 40% equities (SPY)"
    elif risk_level == "Medium":
        initial_recommendation = "40% bonds (AGG), 60% equities (SPY)"
    elif risk_level == "High":
        initial_recommendation = "20% bonds (AGG), 80% equities (SPY)"
    else: initial_recommendation = "0% bonds (AGG), 100% equities (SPY)"
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you, {} for your information;
            based on the given information, we recommend the following {}.
            """.format(
                first_name, initial_recommendation
            ),
        },
                )

    ### YOUR FINAL INVESTMENT RECOMMENDATION CODE ENDS HERE ###

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information;
            based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(
                first_name, initial_recommendation
            ),
        },
                )
           

### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "RecommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
