__author__ = "Ruben Svensson"
__copyright__ = """

    Copyright 2017-2019 Modern Ancient Instruments Networked AB, dba Elk

    elkpy is free software: you can redistribute it and/or modify it under the terms of the
    GNU General Public License as published by the Free Software Foundation, either version 3
    of the License, or (at your option) any later version.

    elkpy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along with elkpy.  If
    not, see <http://www.gnu.org/licenses/>.
"""
__license__ = "GPL-3.0"

import grpc
from . import sushierrors
from . import grpc_gen
from . import sushi_info_types as info_types
from typing import List

###############################
# Main sushi controller class #
###############################

class SushiController(object):
    '''
    A class to control sushi via gRPC.

    Attributes:
        _stub (SushiControllerStub): Connection stubs to the gRPC interface implemented in sushi.
    '''
    def __init__(self,
                 address = 'localhost:51051',
                 sushi_proto_def = '/usr/share/sushi/sushi_rpc.proto'):
        '''
        The constructor for the SushiController class.

        Parameters:
            address (str): 'ip-addres:port' The ip-addres and port at which to connect to sushi.
            sushi_proto_def (str): path to .proto file with SUSHI's gRPC services definition
        '''
        try:
            channel = grpc.insecure_channel(address)
        except AttributeError as e:
            raise TypeError("Parameter address = {}. Should be a string containing the ip-address and port of sushi ('ip-address:port')".format(address)) from e

        self._sushi_proto, self._sushi_grpc = grpc_gen.modules_from_proto(sushi_proto_def)
        self._stub = self._sushi_grpc.SushiControllerStub(channel)


    # rpc GetTracks(GenericVoidValue) returns (TrackInfoList) {}
    def get_tracks(self) -> List[info_types.TrackInfo]:
        '''
        Gets a list of all available track.

        Returns:
            List[info_types.TrackInfo]: A list with the info of all the available tracks.
        '''
        try:
            response = self._stub.GetTracks(self._sushi_proto.GenericVoidValue())

            track_info_list = []
            for track_info in response.tracks:
                track_info_list.append(info_types.TrackInfo(track_info))
            return track_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e)


    ####################
    # // Track control #
    ####################

    # rpc GetTrackId(GenericStringValue) returns (TrackIdentifier) {}
    def get_track_id(self, track_name: str) -> int:
        '''
        Get the id of a track from its name.

        Parameters:
            track_name (str): The name of the track.

        Returns:
            int: The id of the track matching the name.
        '''
        try:
            response = self._stub.GetTrackId(self._sushi_proto.GenericStringValue(
                value = track_name
            ))
            return response.id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track name: {}".format(track_name))

    # rpc GetTrackInfo(TrackIdentifier) returns (TrackInfo) {}
    def get_track_info(self, track_identifier: int) -> info_types.TrackInfo:
        '''
        Get the info of a track from its id.

        Parameters:
            track_identifier (int): The id of the track to get the info from.

        Returns:
            info_types.TrackInfo: The info of the track matching the id.
        '''
        try:
            response = self._stub.GetTrackInfo(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))
            return info_types.TrackInfo(response)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))

    # rpc GetTrackProcessors(TrackIdentifier) returns (ProcessorInfoList) {}
    def get_track_processors(self, track_identifier: int) -> List[info_types.ProcessorInfo]:
        '''
        Get a list of processors assigned on the specified track.

        Parameters:
            track_identifier (int): The id of the track to get the processor list from.

        Returns:
            List[info_types.ProcessorInfo]: A list of the info of the processors assigned to the track matching the id.
        '''
        try:
            response = self._stub.GetTrackProcessors(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))

            processor_info_list = []
            for processor_info in response.processors:
                processor_info_list.append(info_types.ProcessorInfo(processor_info))

            return processor_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))

    # rpc GetTrackParameters(TrackIdentifier) returns (ParameterInfoList) {}
    def get_track_parameters(self, track_identifier: int) -> List[info_types.ParameterInfo]:
        '''
        Get a list of parameters available on the specified track.

        Parameters:
            track_identifier (int): The id of the track to get the parameter list from.

        Returns:
            List[info_types.ParameterInfo]: A list of the info of the parameters assigned to the track matching the id.
        '''
        try:
            response = self._stub.GetTrackParameters(self._sushi_proto.TrackIdentifier(
                id = track_identifier
            ))

            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))

            return parameter_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With track id: {}".format(track_identifier))
    # // list requests left out for now

    ########################
    # // Processor control #
    ########################

    # rpc GetProcessorId (GenericStringValue) returns (ProcessorIdentifier) {}
    def get_processor_id(self, processor_name: str) -> int:
        '''
        Get the id of a processor from its name.

        Parameters:
            processor_name (str): The name of the processor to get the id from.

        Returns:
            int: The id of the processor matching the name.
        '''
        try:
            response = self._stub.GetProcessorId(self._sushi_proto.GenericStringValue(
                value = processor_name
            ))
            return response.id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor name: {}".format(processor_name))

    # rpc GetProcessorInfo (ProcessorIdentifier) returns (ProcessorInfo) {}
    def get_processor_info(self, processor_identifier: int) -> info_types.ProcessorInfo:
        '''
        Get the info of a processor from its id.

        Parameters:
            track_identifier (int): The id of the processor to get the info from.

        Returns:
            info_types.ProcessorInfo: The info of the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorInfo(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            return info_types.ProcessorInfo(response)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    # rpc GetProcessorBypassState (ProcessorIdentifier) returns (GenericBoolValue) {}
    def get_processor_bypass_state(self, processor_identifier: int) -> bool:
        '''
        Get the bypass state of the specified processor.

        Parameters:
            processor_identifier (int): The id of processor to get the bypass state from.

        Returns:
            bool: The bypass state of the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorBypassState(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    # rpc SetProcessorBypassState (ProcessorBypassStateSetRequest) returns (GenericVoidValue) {}
    def set_processor_bypass_state(self, processor_identifier: int, bypass_state: bool) -> None:
        '''
        Set the bypass state of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to set the bypass state of.
            bypass_sate (bool): The bypass state of the processor matching the id.
        '''
        try:
            self._stub.SetProcessorBypassState(self._sushi_proto.ProcessorBypassStateSetRequest(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                value = bypass_state
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, bypass state: {}".format(processor_identifier, bypass_state))

    # rpc GetProcessorCurrentProgram (ProcessorIdentifier) returns (ProgramIdentifier) {}
    def get_processor_current_program(self, processor_identifier: int) -> int:
        '''
        Get the id of the current program of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the current program id from.

        Returns:
            int: The id of the processors current program.
        '''
        try:
            response = self._stub.GetProcessorCurrentProgram(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            return response.program

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    # rpc GetProcessorCurrentProgramName (ProcessorIdentifier) returns (GenericStringValue) {}
    def get_processor_current_program_name(self, processor_identifier: int) -> str:
        '''
        Get the name of the current program of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the current program name from.

        Returns:
            str: The name of the processors current program.
        '''
        try:
            response = self._stub.GetProcessorCurrentProgramName(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    # rpc GetProcessorProgramName (ProcessorProgramIdentifier) returns (GenericStringValue) {}
    def get_processor_program_name(self, processor_identifier: int, program_identifier: int) -> str:
        '''
        Get the name of the specified program on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the program name from.
            program_identifier (int): The id of the program to get the name of.

        Returns:
            str: The name of the program matching the processor and program id.
        '''
        try:
            response = self._stub.GetProcessorProgramName(self._sushi_proto.ProcessorProgramIdentifier(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                program = program_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, program id: {}".format(processor_identifier, program_identifier))

    # rpc GetProcessorPrograms (ProcessorIdentifier) returns (ProgramInfoList) {}
    def get_processor_programs(self, processor_identifier: int) -> List[info_types.ProgramInfo]:
        '''
        Get a list of the available programs of the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the programs from.

        Returns:
            List[info_types.ProgramInfo]: A list of the programs available to the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorPrograms(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))

            program_info_list = []
            for program_info in response.programs:
                program_info_list.append(info_types.ProgramInfo(program_info))

            return program_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    # rpc SetProcessorProgram (ProcessorProgramSetRequest) returns (GenericVoidValue) {}
    def set_processor_program(self, processor_identifier: int, program_identifier: int) -> None:
        '''
        Set the program of the specified processor to the one matching the specified program id.

        Parameters:
            processor_identifier (int): The id of the processor to set the program of.
            program_identifier (int): The id of the program to set.
        '''
        try:
            self._stub.SetProcessorProgram(self._sushi_proto.ProcessorProgramSetRequest(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                program = self._sushi_proto.ProgramIdentifier(program = program_identifier)
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, program id: {}".format(processor_identifier, program_identifier))

    # rpc GetProcessorParameters (ProcessorIdentifier) returns (ParameterInfoList) {}
    def get_processor_parameters(self, processor_identifier: int) -> List[info_types.ParameterInfo]:
        '''
        Get a list of the parameters available to the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameters from.

        Returns:
            List[info_types.ParameterInfo]: A list of the parameters available to the processor matching the id.
        '''
        try:
            response = self._stub.GetProcessorParameters(self._sushi_proto.ProcessorIdentifier(
                id = processor_identifier
            ))

            parameter_info_list = []
            for parameter_info in response.parameters:
                parameter_info_list.append(info_types.ParameterInfo(parameter_info))

            return parameter_info_list

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}".format(processor_identifier))

    # // list requests left out

    ########################
    # // Parameter control #
    ########################

    # rpc GetParameterId (ParameterIdRequest) returns (ParameterIdentifier) {}
    def get_parameter_id(self, processor_identifier: int, parameter_name: str) -> int:
        '''
        Get the id of the parameter of the specified processor corresponding to the specified parameter name.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter id from.
            parameter_name (str): The name of the parameter to get the id from.

        Returns:
            int: The id of the parameter matching the parameter name.
        '''
        try:
            response = self._stub.GetParameterId(self._sushi_proto.ParameterIdRequest(
                processor = self._sushi_proto.ProcessorIdentifier(id = processor_identifier),
                ParameterName = parameter_name
            ))
            return response.parameter_id

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter name: {}".format(processor_identifier, parameter_name))

    # rpc GetParameterInfo (ParameterIdentifier) returns (ParameterInfo) {}
    def get_parameter_info(self, processor_identifier: int, parameter_identifier: int) -> info_types.ParameterInfo:
        '''
        Get info about the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter info from.
            parameter_identifier (int): The id of the parameter to get the info from.

        Returns:
            info_types.ParameterInfo: Info of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterInfo(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return info_types.ParameterInfo(response)

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    # rpc GetParameterValue(ParameterIdentifier) returns (GenericFloatValue) {}
    def get_parameter_value(self, processor_identifier: int, parameter_identifier: int) -> float:
        '''
        Get the value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter value from.
            parameter_identifier (int): The id of the parameter to get the value from.

        Returns:
            float: The value of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValue(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    # rpc GetParameterValueNormalised(ParameterIdentifier) returns (GenericFloatValue) {}
    def get_parameter_value_in_domain(self, processor_identifier: int, parameter_identifier: int) -> float:
        '''
        Get the normalised value of the parameter matching the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor to get the normalised parameter value from.
            parameter_identifier (int): The id of the parameter to get the normalised value from.

        Returns:
            float: The normalised value of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValueInDomain(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier,parameter_identifier))

    # rpc GetParameterValueAsString(ParameterIdentifier) returns (GenericStringValue) {}
    def get_parameter_value_as_string(self, processor_identifier: int, parameter_identifier: int) -> str:
        '''
        Get the value of the parameter matching the specified parameter on the specified processor as a string.

        Parameters:
            processor_identifier (int): The id of the processor to get the parameter value string from.
            parameter_identifier (int): The id of the parameter to get value string from.

        Returns:
            str: The value as a string of the parameter matching the id.
        '''
        try:
            response = self._stub.GetParameterValueAsString(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    # rpc GetStringPropertyValue(ParameterIdentifier) returns (GenericStringValue) {}
    # TODO: Not implemented in sushi yet
    def get_string_property_value(self, processor_identifier: int, parameter_identifier: int) -> str:
        '''
        CURRENTLY NOT IMPLEMENTED IN SUSHI
        '''
        try:
            response = self._stub.GetStringPropertyValue(self._sushi_proto.ParameterIdentifier(
                processor_id = processor_identifier,
                parameter_id = parameter_identifier
            ))
            return response.value

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}".format(processor_identifier, parameter_identifier))

    # rpc SetParameterValue(ParameterSetRequest) returns (GenericVoidValue) {}
    def set_parameter_value(self, processor_identifier: int, parameter_identifier: int, value: float) -> None:
        '''
        Set the value of the specified parameter on the specified processor.

        Parameters:
            processor_identifier (int): The id of the processor that has the parameter to be changed.
            parameter_identifier (int): The id of the parameter to set the value of.
        '''
        try:
            self._stub.SetParameterValue(self._sushi_proto.ParameterSetRequest(
                parameter = self._sushi_proto.ParameterIdentifier(
                    processor_id = processor_identifier,
                    parameter_id = parameter_identifier
                    ),
                value = value
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}, value: {}".format(processor_identifier, parameter_identifier, value))

    # rpc SetStringPropertyValue(StringPropertySetRequest) returns (GenericVoidValue) {}
    # TODO: Not implemented in sushi yet
    def set_string_property_value(self, processor_identifier: int, parameter_identifier: int, value: str) -> None:
        '''
        CURRENTLY NOT IMPLEMTED IN SUSHI
        '''
        try:
            self._stub.SetStringPropertyValue(self._sushi_proto.StringPropertySetRequest(
                property = self._sushi_proto.ParameterIdentifier(
                    processor_id = processor_identifier,
                    parameter_id = parameter_identifier
                ),
                value = value
            ))

        except grpc.RpcError as e:
            sushierrors.grpc_error_handling(e, "With processor id: {}, parameter id: {}, value: {}".format(processor_identifier, parameter_identifier, value))
