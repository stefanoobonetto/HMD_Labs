# Resume:

- Lab 1: Input: User Input
- Lab 2: NLU --> JSON, intent, slots (bool, int, string)

# LAB 3: Dialogue Manager

we have to map each intent to a system_action.

e.g. pizza_ordering 
- req_info[mising_slots]
- fallback_policy
- confirmation 

---

**User: I want a cheese pizza**

```src
{
    intent : "pizza_ordering", 
    
    slots : {
        pizza_type : "cheese",
        pizza_count : null,
        pizza_size : null,
    }

}
```

**Bot: How many**

---> Ask to fill slot *pizza_count*

**User: I want two of them**

```src
{
    intent : "pizza_ordering", 
    
    slots : {
        pizza_type : "cheese",
        pizza_count : 2,
        pizza_size : null
    }

}
```

**Bot: Which size?**

---> Ask to fill slot *pizza_size*

**User: I would go for medium size**

```src
{
    intent : "pizza_ordering", 
    
    slots : {
        pizza_type : "cheese",
        pizza_count : 2,
        pizza_size : "medium"
    }

}
```

Dialogue State Tracker --> tracks the state of the dialogue (JSOn filled with all the solts during the dialogue). 

## NLU component 

**prompt.txt**

```txt
Identify the user intent from this list: [ramen_ordering, pizza_ordering, pizza_delivery, flight_booking, drink_ordering]
If the intent is ramen_ordering, extract the slots from the input of the user.
The slots are: [brooth, spaghetti_type, ham_on_top, eggs, mushrooms, spring_onion, bamboo_shoots, carrots, seaweed].
If no values are present in the user input you have to put null as the value.
Output them as a json.
```

**input.txt**

```txt
I want to order a ramen with brooth, weath noodles and no eggs.
```

The output we obtain is the following:

```src
{
    intent : "ramen_ordering", 
    
    slots : {
        brooth : "normal",
        spaghetti_type : "weath_noodles", 
        ham_on_top : null,
        egg : "none",
        mushrooms : null,
        spring_onion : null,
        bamboo_shoots : null,
        carrots : null,
        seaweed : null 
    }
}
```

## DM component

We gave him the following prompt:

**prompt.txt**

```txt
You are the Dialogue Manager.
Given the output of the NLU component, you should generate the best action to take from this list:
- request_info(slot), if a slot value is missing (null)
- confirmation(intent), if all slots have been filled
```

**input.txt** is the output of the NLU component

```txt
{
    intent : "ramen_ordering", 
    slots : {
        brooth : "as_side",
        spaghetti_type : "weath_noodles", 
        ham_on_top : null,
        egg : "none",
        mushrooms : null,
        spring_onion : null,
        bamboo_shoots : null,
        carrots : null,
        seaweed : null 
    }
}
```



It would be useful to generate a JSON file like this:

```txt
{
    "NLU" : {
        intent : "ramen_ordering", 
        slots : {
            brooth : "as_side",
            spaghetti_type : "weath_noodles", 
            ham_on_top : null,
            egg : "none",
            mushrooms : null,
            spring_onion : null,
            bamboo_shoots : null,
            carrots : null,
            seaweed : null 
        }
    },
    "DM" : {
        "next_best_action" : "request_info(ham_on_top)"
    }
}
```

In order to continuously fullfill the JSON file.

## NLG component

**prompt.txt**

```txt
You are the NLG component, 
Given the best action classified by the Dialogue Manager Component, you should generate a lexicalized response for the user.
Possible next best actions are:
- request_info(slot_name): you have to ask to the user if   
- confirmation(intent), confirm the task has been completed and the ramen has been ordered
```

**input.txt**

```txt
{
    "NLU" : {
        intent : "ramen_ordering", 
        slots : {
            brooth : "as_side",
            spaghetti_type : "weath_noodles", 
            ham_on_top : null,
            egg : "none",
            mushrooms : null,
            spring_onion : null,
            bamboo_shoots : null,
            carrots : null,
            seaweed : null 
        }
    },
    "DM" : {
        "next_best_action" : "request_info(ham_on_top)"
    }
}
```

We expect an output like this: 

```txt
{
    "NLU" : {
        intent : "ramen_ordering", 
        slots : {
            brooth : "as_side",
            spaghetti_type : "weath_noodles", 
            ham_on_top : null,
            egg : "none",
            mushrooms : null,
            spring_onion : null,
            bamboo_shoots : null,
            carrots : null,
            seaweed : null 
        }
    },
    "DM" : {
        "next_best_action" : "request_info(ham_on_top)"
    },
    "NLG" : {
        "question" : "Excuse me, would you like to add ham on top of your ramen?"
    }
}
```





This may be the inital input, the JSON that need to be fullfill:

```txt
{
    "NLU" : {},
    "DM" : {},
    "NLG" : {},
    ....
}
```


## PIPELINE

1. User Input 
2. [NLU component (Intent classification, slots' values extraction, **INFO EXTRACTION**)] 
3. Meaningful rrepresentation --> [Dialogue Manager (NBA prediction, System action, **DECISION MAKING**)] 
4. Next Best Action 
5. NLG component (Response generation **LEXICALIZATION**)
6. System Response

Now let's build:

user input --> req_for_info --> confirmation

in an **automatic manner**.