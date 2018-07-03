def ded(source, target, is_combine_LCS=True, as_least_cost=False):
    n = len(source)
    m = len(target)

    # ["", "cost", "prev", "" , "direction"]
    d = [([[0, 0, 0, 0, 0]] * (m + 1)) for i in range(n + 1)]

    for i in range(n):
        d[i + 1][0] = [1, i + 1, i, 0, 2]
    for j in range(m):
        d[0][j + 1] = [1, j + 1, 0, j, 3]

    for i in range(n):

        s = source[i]
        for j in range(m):
            t = target[j]
            cost = 1
            if s == t:
                cost = 0

            d[i + 1][j + 1] = [cost, d[i + 1][j][1] + 1, i + 1, j, 3]

            if d[i][j + 1][1] + 1 < d[i + 1][j + 1][1]:
                d[i + 1][j + 1] = [cost, d[i][j + 1][1] + 1, i, j + 1, 2]

            if d[i][j][1] + cost < d[i + 1][j + 1][1]:
                d[i + 1][j + 1] = [cost, d[i][j][1] + cost, i, j, 1]

    rs = dict()


    if as_least_cost:
        least_cost = n + m
        for k in range(m, 0, -1):
            if least_cost > d[n][k][1]:
                least_cost, i, j = d[n][k][1], n, k
        rs["cost"] = least_cost
    else:
        i = n
        j = m
        rs["cost"] = d[n][m][1]
    details = []
    while i != 0 or j != 0:
        prev = d[d[i][j][2]][d[i][j][3]]
        if d[i][j][1] == prev[1]:
            # none difference
            details.append({
                "type": "none",
                "src": str(source[i - 1]),
                "tgt": str(target[j - 1]),
                "src_i": [i - 1],
                "tgt_i": [j - 1],
                "cost": 0
            })
        else:
            # insertion
            if d[i][j][4] == 3:
                details.append({
                    "type": "ins",
                    "src": "",
                    "tgt": str(target[j - 1]),
                    "src_i": [],
                    "tgt_i": [j - 1],
                    "cost": 1
                })

            # deletion
            elif d[i][j][4] == 2:
                details.append({
                    "type": "del",
                    "src": str(source[i - 1]),
                    "tgt": "",
                    "src_i": [i - 1],
                    "tgt_i": [],
                    "cost": 1
                })

            # substitution
            elif d[i][j][4] == 1:
                details.append({
                    "type": "sub",
                    "src": str(source[i - 1]),
                    "tgt": str(target[j - 1]),
                    "src_i": [i - 1],
                    "tgt_i": [j - 1],
                    "cost": 1
                })

        a = d[i][j][2]
        j = d[i][j][3]
        i = a
    rs["detail"] = details[::-1]

    if is_combine_LCS:
        details = []
        last_type = ""
        for detail in rs["detail"]:
            if last_type == detail["type"]:
                last_type = detail["type"]
                src += detail["src"]
                tar += detail["tgt"]
                src_i += detail["src_i"]
                tgt_i += detail["tgt_i"]
                cost += detail["cost"]
            else:
                if last_type != "":
                    details.append({
                        "type": last_type,
                        "src": src,
                        "tgt": tar,
                        "src_i": src_i,
                        "tgt_i": tgt_i,
                        "cost": cost
                    })

                last_type = detail["type"]
                src = detail["src"]
                tar = detail["tgt"]
                src_i = detail["src_i"]
                tgt_i = detail["tgt_i"]
                cost = detail["cost"]

        details.append({
            "type": last_type,
            "src": src,
            "tgt": tar,
            "src_i": src_i,
            "tgt_i": tgt_i,
            "cost": cost
        })

        rs["detail"] = details

    return rs


if __name__ == "__main__":
    rs = ded([a for a in "ABCDE"], [a for a in "ABZDE"])
    print(rs)
