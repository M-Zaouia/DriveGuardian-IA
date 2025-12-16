def analyze_risk(frames_metrics):
    """
    frames_metrics : liste de dicts, chaque élément contient par ex :
        {
            "dt": 0.1,  # durée en secondes
            "lane_status": "center" / "near_line" / "out_of_lane",
            "distance_zone": "safe" / "close" / "very_close",
        }
    Retour : dict risk_summary avec les indicateurs de risque sur tout le trajet.
    """

    # --- 1) Initialiser les compteurs de temps ---
    total_time = 0.0

    time_lane_center = 0.0
    time_lane_near_line = 0.0
    time_lane_out = 0.0

    time_distance_safe = 0.0
    time_distance_close = 0.0
    time_distance_very_close = 0.0

    # pour compter les "épisodes" de risque élevé (distance très dangereuse prolongée)
    nb_high_risk_events = 0
    current_very_close_duration = 0.0   # temps cumulé en very_close en cours

    # --- 2) Parcourir toutes les mesures ---
    for m in frames_metrics:
        dt = m.get("dt", 0.0)
        lane_status = m.get("lane_status", "center")
        distance_zone = m.get("distance_zone", "safe")

        total_time += dt

        # --- Position dans la voie ---
        if lane_status == "center":
            time_lane_center += dt
        elif lane_status == "near_line":
            time_lane_near_line += dt
        elif lane_status == "out_of_lane":
            time_lane_out += dt

        # --- Distance de sécurité ---
        if distance_zone == "safe":
            time_distance_safe += dt
            # si on revient en safe, on "ferme" un éventuel épisode de very_close
            if current_very_close_duration >= 2.0:  # ex : épisode > 2 secondes
                nb_high_risk_events += 1
            current_very_close_duration = 0.0

        elif distance_zone == "close":
            time_distance_close += dt
            # close = pas forcément "épisode de très gros danger",
            # donc on ne touche pas current_very_close_duration ici

        elif distance_zone == "very_close":
            time_distance_very_close += dt
            current_very_close_duration += dt

    # Si la vidéo se termine alors qu'on était "very_close", il faut aussi compter cet épisode
    if current_very_close_duration >= 2.0:
        nb_high_risk_events += 1

    # --- 3) Éviter division par zéro ---
    if total_time == 0:
        # Cas extrême : pas de données
        return {
            "duration_sec": 0.0,
            "ratio_distance_close": 0.0,
            "ratio_distance_very_close": 0.0,
            "ratio_lane_near_line": 0.0,
            "ratio_lane_out": 0.0,
            "ratio_distance_risque": 0.0,
            "ratio_position_risque": 0.0,
            "nb_high_risk_events": 0,
            "risk_level": "inconnu",
            "main_risk": "none",
        }

    # --- 4) Calcul des ratios (pourcentages du temps) ---
    ratio_distance_close = time_distance_close / total_time
    ratio_distance_very_close = time_distance_very_close / total_time
    ratio_lane_near_line = time_lane_near_line / total_time
    ratio_lane_out = time_lane_out / total_time

    ratio_distance_risque = ratio_distance_close + ratio_distance_very_close
    ratio_position_risque = ratio_lane_near_line + ratio_lane_out

    # --- 5) Détermination du niveau de risque global ---
    if ratio_distance_risque < 0.10 and ratio_position_risque < 0.10 and nb_high_risk_events == 0:
        risk_level = "faible"
    elif ratio_distance_risque < 0.30 and ratio_position_risque < 0.25 and nb_high_risk_events <= 3:
        risk_level = "modere"
    else:
        risk_level = "eleve"

    # --- 6) Principale source de risque ---
    if ratio_distance_risque > ratio_position_risque and ratio_distance_risque > 0.15:
        main_risk = "distance"
    elif ratio_position_risque > ratio_distance_risque and ratio_position_risque > 0.15:
        main_risk = "lane_position"
    else:
        main_risk = "none"

    # --- 7) Construire le résumé ---
    risk_summary = {
        "duration_sec": total_time,
        "ratio_distance_close": ratio_distance_close,
        "ratio_distance_very_close": ratio_distance_very_close,
        "ratio_lane_near_line": ratio_lane_near_line,
        "ratio_lane_out": ratio_lane_out,
        "ratio_distance_risque": ratio_distance_risque,
        "ratio_position_risque": ratio_position_risque,
        "nb_high_risk_events": nb_high_risk_events,
        "risk_level": risk_level,      # "faible" / "modere" / "eleve"
        "main_risk": main_risk,        # "distance" / "lane_position" / "none"
    }

    return risk_summary
