# chronoplot

Timeline maker.

## Example

Make file `test`:

    0 10 1 "Ciel nosurge (memories)"
    20 30 1 "Ciel nosurge"
    30 40 1 "Ar nosurge"
    50 60 2 "Ar Tonelico"
    60 70 2 "Ar Tonelico 2"
    70 80 2 "Ar Tonelico 3"

Format is `start_time stop_time group text`.

Run:

    $ chronoplot test
     0 -                      +------------------+
       |                      |   Ciel nosurge   |
       |                      |    (memories)    |
       |                      |                  |
       |                      +------------------+
    13 -                                          
       |                                          
       |                                          
       |                      +------------------+
       |                      |   Ciel nosurge   |
    26 -                      |                  |
       |                      +------------------+
       |                      |                  |
       |                      |    Ar nosurge    |
       |                      |                  |
    40 -                      +------------------+
       |                                          
       |                                          
       |                                          
       | +------------------+                     
    53 - |   Ar Tonelico    |                     
       | |                  |                     
       | +------------------+                     
       | |                  |                     
       | |  Ar Tonelico 2   |                     
    66 - |                  |                     
       | +------------------+                     
       | |                  |                     
       | |  Ar Tonelico 3   |                     
       | |                  |                     
    80 - +------------------+
