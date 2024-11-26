## Natural Language Understanding

### EXAMPLE
- ⁠***UTT***: "I want a cheese pizza"
- ⁠***INTENT***: Pizza ordering
- ⁠***SLOT***: required for intent: 
    - *pizza_type*
    - *pizza_count*
    - *pizza_size*
    - *pizza_dough*

## Structure:

```src
{
    intent : "pizza_ordering", 
    
    slots : {
        pizza_type : "cheese",
        pizza_count : "one",
        pizza_size : null,
        pizza_dough : null 
    }

}
```

## Prompt:

### What to do?

A. Classify intention: pre_defined

B. Extract slot values: also if detected as null

C. return a json file 

D. Sentiment 

### How to do it?

- examples {0, 1, few} shots
- closed/open questions

### Ramen

- spaghetti type 
- vegetables
- ham on top 
- egg or no egg

```src
{
    intent : "ramen_ordering", 
    
    slots : {
        brooth : {"none", "as_side", "normal"}
        spaghetti_type : {"rice_noodles", "weath_noodles", "bucatini", "udon"},
        ham_on_top : {"none", "on_top", "while_cooking"},
        egg : {null, "none", "raw", "well_cooked"},
        mushrooms : {null, "yes", "no"},
        spring_onion : {null, "yes", "no"},
        bamboo_shoots : {null, "yes", "no"},
        carrots : {null, "yes", "no"},
        seaweed : {null, "yes", "no"}
    }
}
```


### slots_ramen.txt
```txt
Identify the user intent from this list: [ramen_ordering, pizza_ordering, pizza_delivery, flight_booking, drink_ordering]
If the intent is ramen_ordering, extract the slots from the input of the user.
The slots are: [brooth, spaghetti_type, ham_on_top, eggs, mushrooms, spring_onion, bamboo_shoots, carrots, seaweed].
If no values are present in the user input you have to put null as the value.
Output them as a json.
```

```bash
sbatch example.sbatch --system-prompt "$(cat slots_ramen.txt)" llama2 "I want to order a ramen soup with brooth as side dish, weath noodles and ham on top. I want to add well cooked eggs. As vegetables I want mushrooms and spring onion."
```