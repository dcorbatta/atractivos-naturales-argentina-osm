[out:json][timeout:180];
area["ISO3166-1"="AR"][admin_level=2]->.ar;
(
  nwr["waterway"="waterfall"](area.ar);
  nwr["tourism"="viewpoint"](area.ar);
  nwr["natural"="peak"](area.ar);
  nwr["natural"="cave_entrance"](area.ar);
);
out center tags;
