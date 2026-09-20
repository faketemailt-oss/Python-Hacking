from . import system,hardware,storage,network,power,browsers,applications
COLLECTORS={"system":system.collect,"hardware":hardware.collect,"storage":storage.collect,"network":network.collect,"power":power.collect,"browsers":browsers.collect,"applications":applications.collect}
def collect(categories): return {n:COLLECTORS[n]() for n in categories if n in COLLECTORS}
