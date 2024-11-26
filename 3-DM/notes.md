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

```src
{
    intent : "ramen_ordering", 
    
    slots : {
        brooth : [null, "none", ], 
        spaghetti_type, 
        ham_on_top, 
        eggs, 
        mushrooms, 
        spring_onion, 
        bamboo_shoots, 
        carrots, 
        seaweed
    }

}
```

slots for **RAMEN ORDERING** --> [
    brooth, spaghetti_type, ham_on_top, eggs, mushrooms, spring_onion, bamboo_shoots, carrots, seaweed]