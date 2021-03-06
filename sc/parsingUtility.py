import json
import re


RUN_ARGS = ["apt-get", "yum", "pip", "git"]


class parsingUtility:

    def __init__(self):
        self.steps = []
        self.data = {}

    def write_out_data(self, file_name="data.json"):
        with open(file_name, "w") as data_file:
            json.dump(self.data, data_file, indent=4)

    def parseCommand(self,cmdString):
        #Directs the command processing to the appropriate function,
        #based on the type of command received.

        #Get the command type from the cmdString
        thisCommand = self.getCommand(cmdString)
        command_data = self.get_command_data(cmdString)

        #Call the appropriate routine based on the command type
        if thisCommand == 'FROM':
            self.parseFROM(command_data)
        elif thisCommand == 'MAINTAINER':
            self.parseMAINTAINER(command_data)
        elif thisCommand == 'RUN':
            self.parseRUN(command_data)
        elif thisCommand == 'CMD':
            self.parseCMD(command_data)
        elif thisCommand == 'LABEL':
            self.parseLABEL(command_data)
        elif thisCommand == 'EXPOSE':
            self.parseEXPOSE(command_data)
        elif thisCommand == 'ENV':
            self.parseENV(command_data)
        elif thisCommand == 'ADD':
            self.parseADD(command_data)
        elif thisCommand == 'COPY':
            self.parseCOPY(command_data)
        elif thisCommand == 'ENTRYPOINT':
            self.parseENTRYPOINT(command_data)
        elif thisCommand == 'VOLUME':
            self.parseVOLUME(command_data)
        elif thisCommand == 'USER':
            self.parseUSER(command_data)
        elif thisCommand == 'WORKDIR':
            self.parseWORKDIR(command_data)
        elif thisCommand == 'ARG':
            self.parseARG(command_data)
        elif thisCommand == 'ONBUILD':
            self.parseONBUILD(command_data)
        elif thisCommand == 'STOPSIGNAL':
            self.parseSTOPSIGNAL(command_data)
        else:
            print "Error parsing command"

        self.steps.append(cmdString)

    def getCommand(self, cmdString):
        #returns command from cmdString, with the assumption
        #that the command is always the first word in the string
        return cmdString.split()[0]

    def get_command_data(self, command):
        """Obtains the second part of the command string.

        Args:
            command (str): The command string.

        Returns: The second part of the command string.

        """
        return command.split(" ", 1)[1]

    def parseFROM(self, data):
        if "from" not in self.data:
            self.data["from"] = []

        new_item = {"string": data}
        if ":" in data:
            split_data = data.split(":")
            new_item["image"] = split_data[0]
            new_item["tag"] = split_data[1]
        elif "@" in data:
            split_data = data.split("@")
            new_item["image"] = split_data[0]
            new_item["digest"] = split_data[1]
        else:
            new_item["image"] = data
            new_item["tag"] = "latest"

        self.data["from"].append(new_item)

    def parseMAINTAINER(self, data):
        self.data["maintainer"] = data

    def parseRUN(self, data):
        if "run" not in self.data:
            self.data["run"] = []

        if data.startswith("["):
            # exec command.
            run_command = data[1:].split(",")
            new_run_command = {
                "executable": run_command[0].strip()[1:-1],
            }
            parameters = []
            for parameter in run_command[1:]:
                parameters.append(parameter.strip()[1:-1])
            new_run_command["parameters"] = parameters

            self.data["run"].append(new_run_command)
        else:
            # shell command.
            commands = data.split("&&")
            new_item = {"original": data}

            for command in commands:
                split_command = command.split()

                if split_command[0] in RUN_ARGS:
                    if "special" not in new_item:
                        new_item["special"] = {}
                    if split_command[0] not in new_item["special"]:
                        new_item["special"][split_command[0]] = []

                    new_item["special"][split_command[0]].append(" ".join(split_command[1:]))

            self.data["run"].append(new_item)

    def parseCMD(self,cmdCMD):
        pass

    def parseLABEL(self, data):
        if "label" not in self.data:
            self.data["label"] = {}

        key_pair_pattern_string = "\"?\w*\"?=\".*?\""
        key_pair_pattern = re.compile(key_pair_pattern_string)

        labels = key_pair_pattern.findall(data)
        for label in labels:
            key, value = tuple([split_part.replace("\"", "") for split_part in label.split("=")])

            self.data["label"][key] = value

    def parseEXPOSE(self, data):
        if "expose" not in self.data:
            self.data["expose"] = []

        self.data["expose"].extend(data.split())

    def parseENV(self, cmdENV):
        pass

    def parseADD(self, data):
        if "add" not in self.data:
            self.data["add"] = []

        if data.startswith("["):
            split_data = json.loads(data)
        else:
            split_data = data.split()

        new_item = {
            "src": split_data[:-1],
            "dest": split_data[-1]
        }

        self.data["add"].append(new_item)

    def parseCOPY(self, data):
        if "copy" not in self.data:
            self.data["copy"] = []

        if data.startswith("["):
            split_data = json.loads(data)
        else:
            split_data = data.split()

        new_item = {
            "src": split_data[:-1],
            "dest": split_data[-1]
        }

        self.data["copy"].append(new_item)

    def parseENTRYPOINT(self, cmdENTRYPOINT):
        pass

    def parseVOLUME(self, data):
        if "volume" not in self.data:
            self.data["volume"] = []

        if data.startswith("["):
            split_data = json.loads(data)
        else:
            split_data = data.split()

        self.data["volume"].extend(split_data)

    def parseUSER(self, data):
        if "user" not in self.data:
            self.data["user"] = []

        self.data["user"].append(data)

    def parseWORKDIR(self, data):
        if "workdir" not in self.data:
            self.data["workdir"] = []

        self.data["workdir"].append(data)

    def parseARG(self, data):
        if "arg" not in self.data:
            self.data["arg"] = []

        split_data = data.split("=")
        new_item = {"name": split_data[0]}

        if len(split_data) > 1:
            new_item["value"] = split_data[1]

        self.data["arg"].append(new_item)

    def parseONBUILD(self, cmdONBUILD):
        pass

    def parseSTOPSIGNAL(self, data):
        self.data["stopsignal"] = data
