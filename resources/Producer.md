# Producer Logic

## Introduction
The first step in this pipeline is data generation. In our case, this task is a bit complex - the reason being that our data is necesarily **stateful**. 
So, it is here where we must start defining our constraints and the scope of the project to make things feasible. 

## Defining Some Data
### Flight Event
Our project centers around flight data - to be more specific, information about airplanes that are currently flying. We first ought to consider what we might
want to analyze. In this case, the `Schema` becomes important to talk about. Rather than figuring out what we want to analyze, we will instead choose to start
by asking "what data is available". Below, I've defined a schema for a `Flight Event` It contains some sample data as well. 
``` JSON
{
  "flight_number": "UA123",
  "aircraft_type": "B767",
  "bearing": 247.5,
  "location": (80.23, 40.24),
  "elevation": 4000,
  "speed": 900,
  "timestamp": "2026-03-01 21:13:33.041222"
}
``` 
The units/types of these are as follows:
```
- flight_number: string (probably an ENUM)
- aircraft_type: string (probably an ENUM)
- bearing: float (in degrees °)
- location: (longitude, latitude) - longitude and latitude themselves being float
- eleveation: float (meters)
- speed: float (kilometers per second km/h)
- timestmap: string (datetime, ISO 8601 format)
```

A `Flight Event` is information about an airplane operating a flight at a certain point in time. Now that we have
a fundamental data point that we ought' to generate, we must consider HOW we will generate such data.
### Flight Lifetime
- Note that we are not generating flight lifetimes that will be consumed. This is internal to the Producer, but
make no mistake; it is CRUCIAL
-----
The `Flight Lifetime` dictates the course of a flight from start to end. It is a sequence of `Flight Event`s.
However, the question is this - how many do we need to generate? We will now address...
### Sector
The `Sector` will be the FOCUS of our project. We will monitor flights that are traveling *through* our airspace!
This is the key; the `Flight Lifetime` is defined by when a flight first enters our airspace and when it leaves;
entering and leaving the `Sector`. Our `Sector` is a small section of Illinois and will look something like:
``` Python
class Sector:
  left: float = -89.0
  right: float = -87.0
  top: float = 42.0
  bottom: float= 40.0
```
Remember, negative for left and right refer to West of prime meridian, while positive for top and bottom represent
North of the Equator. 

Now that we've defined a `Sector`, generating `Flight Event`s that are constrained by `Flight Lifetime`s becomes 
easier - especially with use of a wonderful library called `geodistpy`. 
### Back to Flight Lifetime
The `Flight Lifetime` is a sequence of `Flight Event`s. It starts at the boundary and ends at another boundary. 
If it starts at left, it can end at any point along one of three boundaries. Our next task is to then figure out
how to generate flight events and how many to generate for a flight event. Fortunately, we have all the tools 
we need!
#### Generating Events for a Lifetime
1. Compute the distance using the `geodist()` method (NOTE: METRIC) by feeding the intial and final co-ordinates.
2. Divide by the `speed` attribute (NOTE: This will not change for a flight) and take the floor of the quotient. This will become `N`: the number of *steps* to generate. These steps correspond to second-by-second updates.
3. Use `interpolate()` to generate the points for your path.
4. Generate the requisite flight events for each of those points!
## Putting it All Together
At this point, we've reached a..."trivial" logic, but one that works with reasonable success. Internally, we generate a `Flight Lifetime` - we define a starting location and an ending location, each at certain points along the boundaries. The lifetime will contain a list of events, timestamped, starting and ending at these points. At this point, we only need to emit these points.