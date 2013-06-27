# Insights
Things I have noticed/learned throughout the development of this project in particular. Your mileage may vary.

-   Use keyword arguments when calling constructors from core game logic, because their names change frequently at this stage in development.
    Bad: Thing(1, 2) / Good: Thing(lvl=1, life=2)
