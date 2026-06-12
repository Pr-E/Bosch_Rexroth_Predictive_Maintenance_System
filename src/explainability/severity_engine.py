def determine_severity(
    impact
):

    impact = abs(impact)

    if impact >= 25:

        return "CRITICAL"

    elif impact >= 15:

        return "HIGH"

    elif impact >= 5:

        return "MODERATE"

    elif impact >= 2:

        return "LOW"

    else:

        return "MINIMAL"