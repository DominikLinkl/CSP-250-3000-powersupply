with open("V2/finalV2_UPSCALE/data_logger.h", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.strip() == "// Ausdünnen wenn zu viele Punkte":
        skip = True
        new_lines.append("    // Ausdünnen wenn zu viele Punkte\n")
        new_lines.append("    int step = 1;\n")
        new_lines.append("    if (count > MAX_DISPLAY_POINTS) {\n")
        new_lines.append("        step = count / MAX_DISPLAY_POINTS;\n")
        new_lines.append("    }\n\n")
        new_lines.append("    // 2. Pass: Read and construct JSON\n")
        new_lines.append("    f = LittleFS.open(LOG_FILE_PATH, \"r\");\n")
        new_lines.append("    f.readStringUntil('\\n'); // Skip header\n\n")
        new_lines.append("    int outputCount = 0;\n")
        new_lines.append("    int currentLineIndex = 0;\n")
        new_lines.append("    uint32_t firstTs = 0;\n\n")
        new_lines.append("    while (f.available()) {\n")
        new_lines.append("        String line = f.readStringUntil('\\n');\n")
        new_lines.append("        if (line.length() < 5) continue;\n\n")
        new_lines.append("        int c1 = line.indexOf(',');\n")
        new_lines.append("        int c2 = line.indexOf(',', c1 + 1);\n")
        new_lines.append("        if (c1 < 0 || c2 < 0) continue;\n\n")
        new_lines.append("        uint32_t ts = line.substring(0, c1).toInt();\n\n")
        new_lines.append("        if (ts >= minTime) {\n")
        new_lines.append("            if (currentLineIndex % step == 0) {\n")
        new_lines.append("                float v = line.substring(c1 + 1, c2).toFloat();\n")
        new_lines.append("                float p = line.substring(c2 + 1).toFloat();\n\n")
        new_lines.append("                if (firstTs == 0) firstTs = ts;\n\n")
        new_lines.append("                if (outputCount > 0) json += \",\";\n")
        new_lines.append("                json += \"{\\\"t\\\":\" + String(ts - firstTs);\n")
        new_lines.append("                json += \",\\\"v\\\":\" + String(v, 1);\n")
        new_lines.append("                json += \",\\\"p\\\":\" + String(p, 1) + \"}\";\n")
        new_lines.append("                outputCount++;\n")
        new_lines.append("            }\n")
        new_lines.append("            currentLineIndex++;\n")
        new_lines.append("        }\n")
        new_lines.append("    }\n")
        new_lines.append("    f.close();\n")
    if skip and line.strip().startswith("json +="):
        skip = False

    if not skip:
        new_lines.append(line)

with open("V2/finalV2_UPSCALE/data_logger.h", "w") as f:
    f.writelines(new_lines)
