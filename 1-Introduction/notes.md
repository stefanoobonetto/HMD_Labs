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
