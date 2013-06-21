# Insights
Things I have noticed/learned throughout the development. Not necessarily true for every project! Your mileage may vary.

- Use keyword arguments when calling constructors from core game logic, because these change frequently at this stage in development. Bad: Thing(1, 2) / Good: Thing(lvl=1, life=2)
