from pyopensky.rest import REST

rest: REST = REST()

my_area = (-0.5, 51.3, 0.3, 51.7)

df = rest.states(bounds=my_area)

print(df)
