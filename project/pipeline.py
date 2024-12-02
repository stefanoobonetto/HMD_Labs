from model_query import ModelQuery
from utils import *
from dict_manager import DictManager

if __name__ == "__main__":
    dict_manager = DictManager()
    model_query = ModelQuery()

    try:
        
        print("\n\n\nWelcome to the Ramen Ordering System!\n\n\n")

        # Step 1: NLU - Parse initial user input
        response_NLU = model_query.query_model(
            system_prompt=PROMPT_NLU,
            input_file=USER_INPUT
        )
        print("\n\nNLU response:\n\n", response_NLU)
        
        dict_manager.validate_dict(response_NLU)
    except Exception as e:
        print(f"Error occurred during NLU: {e}")
        exit()

    confirmation_received = False

    while not confirmation_received:
        try:
            # Step 2: DM - Get the next best action
            response_DM = model_query.query_model(
                system_prompt=PROMPT_DM,
                input_file=dict_manager.to_json()  
            )
            print("\n\nDM response:\n\n", response_DM)

            dict_manager.validate_dict(response_DM)

            next_best_action = dict_manager.get_next_best_action()
            # print("\n\nNext best action:\n\n", next_best_action)

            if next_best_action.startswith("confirmation"):
                # Step 3: NLG - Generate confirmation message
                response_NLG = model_query.query_model(
                    system_prompt=PROMPT_NLG,
                    input_file=dict_manager.to_json()
                )
                print("\n\nNLG response:\n\n", response_NLG)

                # Display confirmation and exit the loop
                user_input = input(f"{response_NLG} [yes/no]: ").strip().lower()
                if user_input == "yes":
                    print("Order confirmed. Exiting dialogue.")
                    confirmation_received = True
                else:
                    print("Order not confirmed. Exiting dialogue.")
                    exit()

            elif next_best_action.startswith("request_info"):
                slot_to_fill = next_best_action.split('(')[-1].strip(')')

                if dict_manager.get_slot_value(slot_to_fill) in (None, "null"):
                    # Ask user for the required information
                    response_NLG = model_query.query_model(
                        system_prompt=PROMPT_NLG,
                        input_file=dict_manager.to_json()
                    )
                    print("\n\nNLG response:\n\n")

                    user_input = input(response_NLG).strip()

                    # Step 4: Pass user's input to DM to update json dictionary with the new slot value 
                    update_slot_prompt = (
                        f"Given the previous dictionary: {dict_manager.to_json()}, "
                        f"update the slot '{slot_to_fill}' value based on the user input. "
                        "Consider the following valid values for the slots:\n\n"
                        "broth: {null, \"none\", \"pork\", \"chicken\"}\n"
                        "spaghetti_type: {null, \"rice_noodles\", \"wheat_noodles\", \"bucatini\", \"udon\"}\n"
                        "egg: {null, \"no\", \"yes\"}\n"
                        "seaweed: {null, \"yes\", \"no\"}\n"
                        "Do not modify other slots different from the one is asked to be filled."
                        "Return only the updated dictionary, with the old slots values and the new one of the one asked."
                    )

                    response_DM_update = model_query.query_model(
                        system_prompt=update_slot_prompt,
                        input_file=user_input
                    )

                    # print("\n\nDM update response:\n\n", response_DM_update)

                    dict_manager.validate_dict(response_DM_update)

            else:
                print("Unhandled next_best_action. Exiting dialogue.")
                exit()

        except Exception as e:
            print(f"Error occurred during DM or NLG: {e}")
            exit()
