SELECT pretestUser2019.name, pretestUser2019.groups, pretestXapi2019.verb, pretestXapi2019.matrixcode, pretestXapi2019.description
FROM pretestUser2019
INNER JOIN pretestXapi2019
ON pretestUser2019.searchcode=pretestXapi2019.searchcode
WHERE pretestXapi2019.verb = "solved"