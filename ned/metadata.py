from bidict import bidict

NED_ACTIVITIES = bidict({"Providing": 1, "Consuming": 2})

NED_CLASSIFICATIONS = bidict({"Backcast": 1, "Current": 2, "Forecast": 3})

NED_GRANULARITIES = bidict(
    {"10 minutes": 3, "15 minutes": 4, "Hour": 5, "Day": 6, "Month": 7, "Year": 8}
)

NED_GRANULARITY_TIME_ZONES = bidict({"UTC": 0, "CET (Central European Time)": 1})

NED_POINTS_NETHERLANDS = bidict({"Nederland": 0})

NED_POINTS_PROVINCES = bidict(
    {
        "Groningen": 1,
        "Friesland": 2,
        "Drenthe": 3,
        "Overijssel": 4,
        "Flevoland": 5,
        "Gelderland": 6,
        "Utrecht": 7,
        "Noord-Holland": 8,
        "Zuid-Holland": 9,
        "Zeeland": 10,
        "Noord-Brabant": 11,
        "Limburg": 12,
    }
)

NED_POINTS_OFFSHORE = bidict(
    {
        "Offshore": 14,
        "Windpark Luchterduinen": 28,
        "Windpark Princes Amalia": 29,
        "Windpark Egmond aan Zee": 30,
        "Windpark Gemini": 31,
        "Windpark Borselle I&II": 33,
        "Windpark Borselle III&IV": 34,
        "Windpark Hollandse Kust Zuid": 35,
        "Windpark Hollandse Kust Noord": 36,
    }
)

NED_POINTS = bidict(
    {**NED_POINTS_NETHERLANDS, **NED_POINTS_PROVINCES, **NED_POINTS_OFFSHORE}
)

NED_TYPES = bidict(
    {
        "All": 0,
        "Wind": 1,
        "Solar": 2,
        "Biogas": 3,
        "HeatPump": 4,
        "Cofiring": 8,
        "Geothermal": 9,
        "Other": 10,
        "Waste": 11,
        "BioOil": 12,
        "Biomass": 13,
        "Wood": 14,
        "WindOffshore": 17,
        "FossilGasPower": 18,
        "FossilHardCoal": 19,
        "Nuclear": 20,
        "WastePower": 21,
        "WindOffshoreB": 22,
        "NaturalGas": 23,
        "Biomethane": 24,
        "BiomassPower": 25,
        "OtherPower": 26,
        "ElectricityMix": 27,
        "GasMix": 28,
        "GasDistribution": 31,
        "WKK Total": 35,
        "SolarThermal": 50,
        "WindOffshoreC": 51,
        "IndustrialConsumersGasCombination": 53,
        "IndustrialConsumersPowerGasCombination": 54,
        "LocalDistributionCompaniesCombination": 55,
        "AllConsumingGas": 56,
    }
)
