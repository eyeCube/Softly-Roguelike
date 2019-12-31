rads = 15
sick = 4
expo = 32
pain = 64
fear = 43
bleed = 0
rust = 0
rot = 0
wet = 0
gauges=[]
lgauges=[]
if rads > 0:
    lgauges.append( (rads, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('radiation'), a=rads ),) )
if sick > 0:
    lgauges.append( (sick, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('sickness'), a=sick ),) )
if expo > 0:
    lgauges.append( (expo, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('exposure'), a=expo ),) )
if pain > 0:
    lgauges.append( (pain, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('pain'), a=pain ),) )
if fear > 0:
    lgauges.append( (fear, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('fear'), a=fear ),) )
if bleed > 0:
    lgauges.append( (bleed, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('bleed'), a=bleed ),) )
if rust > 0:
    lgauges.append( (rust, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('rust'), a=rust ),) )
if rot > 0:
    lgauges.append( (rot, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('rot'), a=rot ),) )
if wet > 0:
    lgauges.append( (wet, "{v:>32} : {a:<6}\n".format(
            v="* {}".format('wetness'), a=wet ),) )
# sort
lgauges.sort(key = lambda x: x[0], reverse=True)
print(lgauges)
