# -*- generated by 1.0.9 -*-
import da
PatternExpr_483 = da.pat.TuplePattern([da.pat.ConstantPattern('ACK'), da.pat.FreePattern('sender')])
PatternExpr_502 = da.pat.TuplePattern([da.pat.ConstantPattern('Get_configuration'), da.pat.FreePattern('client'), da.pat.FreePattern('client_name'), da.pat.FreePattern('client_id'), da.pat.FreePattern('client_public_key')])
PatternExpr_684 = da.pat.TuplePattern([da.pat.ConstantPattern('wedge'), da.pat.FreePattern('hist'), da.pat.FreePattern('replica_id')])
PatternExpr_860 = da.pat.TuplePattern([da.pat.ConstantPattern('caught_up'), da.pat.FreePattern('hash_running_state'), da.pat.FreePattern('replica_id')])
PatternExpr_946 = da.pat.TuplePattern([da.pat.ConstantPattern('response_get_running_state'), da.pat.ConstantPattern(None), da.pat.ConstantPattern(None)])
PatternExpr_972 = da.pat.TuplePattern([da.pat.ConstantPattern('Reconfiguration'), da.pat.FreePattern('sender'), da.pat.FreePattern('proof_of_misbehavior')])
PatternExpr_1034 = da.pat.TuplePattern([da.pat.ConstantPattern('response_get_running_state'), da.pat.FreePattern('replica_id'), da.pat.FreePattern('replica_running_state')])
PatternExpr_1489 = da.pat.TuplePattern([da.pat.ConstantPattern('ACK'), da.pat.ConstantPattern(None)])
PatternExpr_1512 = da.pat.ConstantPattern('Shutdown')
PatternExpr_1496 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('ACK'), da.pat.ConstantPattern(None)])])
PatternExpr_1516 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.ConstantPattern('Shutdown')])
PatternExpr_955 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.FreePattern(None)]), da.pat.TuplePattern([da.pat.ConstantPattern('response_get_running_state'), da.pat.ConstantPattern(None), da.pat.ConstantPattern(None)])])
_config_object = {}
from nacl.hash import sha256
from nacl.encoding import HexEncoder
from nacl.signing import SigningKey, VerifyKey
from nacl.exceptions import BadSignatureError
from ast import literal_eval
replica_module = da.import_da('replica')
from time import time
from config import *
import read_config

class Olympus(da.DistProcess):

    def __init__(self, procimpl, props):
        super().__init__(procimpl, props)
        self._OlympusReceivedEvent_4 = []
        self._OlympusReceivedEvent_7 = []
        self._OlympusReceivedEvent_8 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_0', PatternExpr_483, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Olympus_handler_482]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_1', PatternExpr_502, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Olympus_handler_501]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_2', PatternExpr_684, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Olympus_handler_683]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_3', PatternExpr_860, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Olympus_handler_859]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_4', PatternExpr_946, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_5', PatternExpr_972, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Olympus_handler_971]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_6', PatternExpr_1034, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Olympus_handler_1033]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_7', PatternExpr_1489, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_OlympusReceivedEvent_8', PatternExpr_1512, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[])])

    def setup(self, name, num_replicas, num_failures, all_replica_conf_failures, head_timeout, replica_timeout, **rest_1538):
        super().setup(name=name, num_replicas=num_replicas, num_failures=num_failures, all_replica_conf_failures=all_replica_conf_failures, head_timeout=head_timeout, replica_timeout=replica_timeout, **rest_1538)
        self._state.name = name
        self._state.num_replicas = num_replicas
        self._state.num_failures = num_failures
        self._state.all_replica_conf_failures = all_replica_conf_failures
        self._state.head_timeout = head_timeout
        self._state.replica_timeout = replica_timeout
        self._state.state = 'NORMAL'
        self._state.num_failures = self._state.num_failures
        self._state.replicas = dict()
        self._state.replica_private_keys = list()
        self._state.replica_public_keys = list()
        self._state.head = None
        self._state.tail = None
        self._state.running_state_validated = 0
        self._state.quorum = list()
        self._state.quorum_replicas = list()
        self._state.longest_history = list()
        self._state.chosen_running_state = None
        self._state.running_states_received = 0
        self._state.ignore_further_caught_up_messages = 0
        self._state.private_key = SigningKey.generate()
        self._state.public_key = self._state.private_key.verify_key.encode(encoder=HexEncoder)
        self._state.configuration_number = 0
        self._state.client_keys = {}
        all_replica_failures = self._state.all_replica_conf_failures.get(self._state.configuration_number, {})
        for i in range(self._state.num_replicas):
            replica_failures = all_replica_failures.get(i, {})
            running_state = dict()
            if (i == 0):
                replica = self.new(replica_module.Replica, args=(i, 'Head', running_state, replica_failures, self._state.head_timeout, self._state.public_key))
                self._state.head = replica
            elif (i == (self._state.num_replicas - 1)):
                replica = self.new(replica_module.Replica, args=(i, 'Tail', running_state, replica_failures, self._state.replica_timeout, self._state.public_key))
                self._state.tail = replica
            else:
                replica = self.new(replica_module.Replica, args=(i, ('Replica ' + str(i)), running_state, replica_failures, self._state.replica_timeout, self._state.public_key))
            self._state.replicas[i] = replica
            replica_name = ('Replica ' + str(i))
            self.output_wrapper('Olympus created replica process: {}'.format(replica_name))
            signing_key = SigningKey.generate()
            verify_key = signing_key.verify_key.encode(encoder=HexEncoder)
            self.output_wrapper('Olympus created keys for replica process: {}. Public key: {}'.format(replica_name, str(verify_key)))
            self._state.replica_private_keys.append(signing_key)
            self._state.replica_public_keys.append(verify_key)

    def run(self):
        for (i, r) in self._state.replicas.items():
            self._start(r)
            self.sign_and_send(('Configuration', self._id, self._state.replicas, self._state.head, self._state.tail, [self._state.replica_public_keys, self._state.configuration_number]), r)
            self.send(('Key', self._state.replica_private_keys[i]), to=r)
        super()._label('_st_label_1486', block=False)
        _st_label_1486 = 0
        while (_st_label_1486 == 0):
            _st_label_1486 += 1
            if PatternExpr_1496.match_iter(self._OlympusReceivedEvent_7, SELF_ID=self._id):
                _st_label_1486 += 1
            else:
                super()._label('_st_label_1486', block=True)
                _st_label_1486 -= 1
        super()._label('_st_label_1509', block=False)
        _st_label_1509 = 0
        while (_st_label_1509 == 0):
            _st_label_1509 += 1
            if PatternExpr_1516.match_iter(self._OlympusReceivedEvent_8, SELF_ID=self._id):
                _st_label_1509 += 1
            else:
                super()._label('_st_label_1509', block=True)
                _st_label_1509 -= 1

    def begin_reconfiguration(self):
        if (self._state.state == 'RECONFIGURATION'):
            self.output_wrapper('System is already in reconfiguration. Ignoring new reconfiguration command.')
            return
        self._state.state = 'RECONFIGURATION'
        self.output('Changing states of replicas from old configuration to IMMUTABLE and spawning new replicas in the new configuration.')
        for (i, r) in self._state.replicas.items():
            self.send('Immutable', to=r)
        self.select_quorum()

    def select_quorum(self):
        self.output_wrapper(('Sending wedge requests: checking replicas: ' + str(self._state.replicas)))
        for (i, r) in self._state.replicas.items():
            self.output_wrapper(('Sending wedge requests to replica: ' + str(i)))
            self.send('wedge_request', to=r)

    def on_successful_quorum(self):
        for (i, r) in enumerate(self._state.quorum_replicas):
            gap = [j for j in self._state.longest_history if (not (j in self._state.quorum[i]))]
            self.send(('catch_up', gap), to=self._state.replicas[r])

    def validate_order_proof(self, order_p):
        (slot_number, operation, configuration, order_stmt) = order_p
        for stmt in order_stmt:
            if ((not (stmt[0] == slot_number)) or (not (stmt[1] == operation)) or (not (stmt[2] == configuration))):
                return False
        return True

    def get_running_state_from_quorum(self):
        self.output_wrapper('Getting the running state from the quorum.')
        for (i, r) in enumerate(self._state.quorum_replicas):
            if (not self._state.running_state_validated):
                self.send('get_running_state', to=self._state.replicas[r])
                super()._label('_st_label_943', block=False)
                _st_label_943 = 0
                while (_st_label_943 == 0):
                    _st_label_943 += 1
                    if PatternExpr_955.match_iter(self._OlympusReceivedEvent_4, SELF_ID=self._id):
                        _st_label_943 += 1
                    else:
                        super()._label('_st_label_943', block=True)
                        _st_label_943 -= 1
                else:
                    if (_st_label_943 != 2):
                        continue
                if (_st_label_943 != 2):
                    break

    def validate_proof_of_misbehavior(self, proof_of_misbehavior):
        (result, result_proof) = proof_of_misbehavior
        if (len(result_proof) < (self._state.num_failures + 1)):
            return True
        majority = 0
        hash = self.calculate_hash(result)
        for i in result_proof:
            if (hash == i[1]):
                majority += 1
        if (majority < ((2 * self._state.num_failures) + 1)):
            return True
        return False

    def calculate_hash(self, val):
        if isinstance(val, str):
            return sha256(str.encode(val), encoder=HexEncoder)
        elif isinstance(val, dict):
            return sha256(str.encode(str(val)), encoder=HexEncoder)
        return sha256(val, encoder=HexEncoder)

    def sign_and_send(self, data, to_):
        data = list(data)
        data[(- 1)] = self._state.private_key.sign(str(data[(- 1)]).encode('utf-8'))
        self.send(tuple(data), to=to_)

    def verify_data_with_key(self, data, pub_key):
        try:
            pub_key.verify(data)
            return literal_eval(data.message.decode('utf-8'))
        except BadSignatureError:
            return None

    def init_new_configuration(self, new_running_state):
        self.output('Shutting down replicas from old configuration.')
        for (i, r) in self._state.replicas.items():
            self.send('Shutdown', to=r)
        self._state.configuration_number += 1
        self._state.replicas = dict()
        self._state.replica_private_keys = list()
        self._state.replica_public_keys = list()
        self._state.head = None
        self._state.tail = None
        all_replica_failures = self._state.all_replica_conf_failures.get(self._state.configuration_number, {})
        for i in range(self._state.num_replicas):
            replica_failures = all_replica_failures.get(i, {})
            if (i == 0):
                replica = self.new(replica_module.Replica, args=(i, 'Head', new_running_state, replica_failures, self._state.head_timeout, self._state.public_key))
                self._state.head = replica
            elif (i == (self._state.num_replicas - 1)):
                replica = self.new(replica_module.Replica, args=(i, 'Tail', new_running_state, replica_failures, self._state.replica_timeout, self._state.public_key))
                self._state.tail = replica
            else:
                replica = self.new(replica_module.Replica, args=(i, ('Replica ' + str(i)), new_running_state, replica_failures, self._state.replica_timeout, self._state.public_key))
            self._state.replicas[i] = replica
            replica_name = ('Replica ' + str(i))
            self.output_wrapper('Olympus created replica process: {}'.format(replica_name))
            signing_key = SigningKey.generate()
            verify_key = signing_key.verify_key.encode(encoder=HexEncoder)
            self.output_wrapper('Olympus created keys for replica process: {}. Public key: {}'.format(replica_name, str(verify_key)))
            self._state.replica_private_keys.append(signing_key)
            self._state.replica_public_keys.append(verify_key)
        self._state.running_state_validated = 0
        self._state.quorum = list()
        self._state.quorum_replicas = list()
        self._state.longest_history = list()
        self._state.chosen_running_state = None
        self._state.running_states_received = 0
        self._state.ignore_further_caught_up_messages = 0
        for (i, r) in self._state.replicas.items():
            self._start(r)
            self.sign_and_send(('Configuration', self._id, self._state.replicas, self._state.head, self._state.tail, [self._state.replica_public_keys, self._state.configuration_number]), r)
            self.send(('Key', self._state.replica_private_keys[i]), to=r)
        self._state.state = 'NORMAL'
        self.output_wrapper('Reconfiguration is successful.')

    def output_wrapper(self, log):
        self.output('[{}][TS: {}]'.format(self._state.name, str(time())), log)

    def _Olympus_handler_482(self, sender):
        self.output_wrapper((('ACK from ' + str(sender)) + '.'))
    _Olympus_handler_482._labels = None
    _Olympus_handler_482._notlabels = None

    def _Olympus_handler_501(self, client, client_name, client_id, client_public_key):
        if (not (self._state.state == 'NORMAL')):
            return
        self._state.client_keys[client_id] = VerifyKey(client_public_key, encoder=HexEncoder)
        self.send(('Configuration', self._state.replicas, self._state.head), to=client)
        self.send(('Keys', self._state.replica_public_keys, self._state.public_key), to=client)
        for (i, r) in self._state.replicas.items():
            self.send(('Client_keys', client_id, client_public_key), to=r)
        self.output_wrapper('Received public key: {} from client: {}'.format(str(client_public_key), str(client_name)))
        self.output_wrapper((('Configuration sent to ' + str(client_name)) + '.'))
    _Olympus_handler_501._labels = None
    _Olympus_handler_501._notlabels = None

    def _Olympus_handler_683(self, hist, replica_id):
        self.output_wrapper(('Wedge message from Replica ' + str(replica_id)))
        if (len(self._state.quorum) < (self._state.num_failures + 1)):
            for order_p in hist:
                if (not self.validate_order_proof(order_p)):
                    return
            for i in range(len(hist)):
                if (i < len(self._state.longest_history)):
                    order_p = hist[i]
                    order_p_lh = self._state.longest_history[i]
                    if (not ((order_p[0] == order_p_lh[0]) and (order_p[1] == order_p_lh[1]) and (order_p[2] == order_p_lh[2]))):
                        return
            self._state.quorum.append([o_p[:(- 1)] for o_p in hist])
            self._state.quorum_replicas.append(replica_id)
            if (len(hist) > len(self._state.longest_history)):
                self._state.longest_history = [o_p[:(- 1)] for o_p in hist]
            if (len(self._state.quorum) == (self._state.num_failures + 1)):
                self.on_successful_quorum()
    _Olympus_handler_683._labels = None
    _Olympus_handler_683._notlabels = None

    def _Olympus_handler_859(self, hash_running_state, replica_id):
        self.output_wrapper(('Caught up message received from Replica ' + str(replica_id)))
        if self._state.ignore_further_caught_up_messages:
            return
        if (not ((self._state.chosen_running_state == None) or (hash_running_state == self._state.chosen_running_state))):
            self.output_wrapper("Chosen quorum is not valid as the hash of all running states don't match.")
            self.output_wrapper('Selecting a new quorum.')
            self._state.ignore_further_caught_up_messages = 1
            self.select_quorum()
            return
        self._state.running_states_received += 1
        self._state.chosen_running_state = hash_running_state
        if (self._state.running_states_received == len(self._state.quorum)):
            self.get_running_state_from_quorum()
    _Olympus_handler_859._labels = None
    _Olympus_handler_859._notlabels = None

    def _Olympus_handler_971(self, sender, proof_of_misbehavior):
        self.output_wrapper((('Reconfiguration request received from ' + str(sender)) + '.'))
        if ((isinstance(proof_of_misbehavior, int) and (proof_of_misbehavior == self._state.configuration_number)) or (isinstance(proof_of_misbehavior, list) and self.validate_proof_of_misbehavior(proof_of_misbehavior))):
            self.output_wrapper((('Reconfiguration request sent by ' + str(sender)) + ' is valid. Starting reconfiguration.'))
            self.begin_reconfiguration()
        else:
            self.output_wrapper((('Proof of misbehavior sent by ' + str(sender)) + " is not valid. If it is sent by replica, its configuration doesn't match and if its sent by client, proof of misbehavior is invalid."))
    _Olympus_handler_971._labels = None
    _Olympus_handler_971._notlabels = None

    def _Olympus_handler_1033(self, replica_id, replica_running_state):
        self.output_wrapper((('Response to get_running_state from Replica ' + str(replica_id)) + ' received by Olympus.'))
        self.output_wrapper('Validating the running_state with the quorum.')
        if (self.calculate_hash(replica_running_state) == self._state.chosen_running_state):
            self._state.running_state_validated = 1
            self.init_new_configuration(replica_running_state)
    _Olympus_handler_1033._labels = None
    _Olympus_handler_1033._notlabels = None
