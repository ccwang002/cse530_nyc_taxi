fileName = 'ny_weather_2015-2016.csv'
targetFile = open( fileName.split('.')[0]+'_normalize.csv' , 'w')
with open(fileName) as f:

  #skip header lines
  for x in range(5):
    headLine = next(f);
    targetFile.write(headLine);

  #format header
  heading = next(f).split();
  newHeading =  "%s %10s %15s %5s\n" % (heading[0], heading[1], heading[2], heading[-3])
  targetFile.write(newHeading);

  # start reading data
  for line in f:
    words = line.split();
    time = words[2];
    p01m = words[-3];
    temperature = words[3];

    # skip if percipitation data is missing or trace
    if p01m == 'M' or p01m =='T':
      continue;

    # skip if temperature data is missing or trace
    if temperature == 'M' or temperature =='T':
      continue;

    temperature = float(temperature);
    # skip temperature limit for snow
    if temperature <= 0:
      continue;

    p01m = float(p01m);
    minute = float(time.split(":")[1]);

    if minute == 0:
      p01hour =  p01m * 3600;
    else:
      p01hour =  p01m/(minute*60) * 3600;

    p01hour = round( p01hour, 2); # round to 2 decimal place
    words[-3] = str(p01hour);

    newLine =  "%s %15s %s %8s %5s\n" % (words[0], words[1], words[2], words[3], words[-3])
    targetFile.write(newLine);


    #print words;
    #print words[2];
    #print words[-3];
    #print time.split(":");
    #print minute;
    #print p01hour;
    

