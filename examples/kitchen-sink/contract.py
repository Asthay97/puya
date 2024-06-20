import typing

from algopy import ARC4Contract, Box, BoxMap, BoxRef, LocalState, GlobalState, Bytes, Global, String, Txn, UInt64, arc4, subroutine, Account, Application, Asset

StaticInts: typing.TypeAlias = arc4.StaticArray[arc4.UInt8, typing.Literal[4]]

class UserStruct(arc4.Struct):
    name: arc4.String
    id: arc4.UInt64
    asset: arc4.UInt64
class KitchenSink(ARC4Contract):
    def __init__(self) -> None:
        ## Local storage
        self.local_int = LocalState(UInt64) # Uint64
        self.local_bytes = LocalState(Bytes) # Bytes        
        self.local_bool = LocalState(bool) #Bool

        self.local_asset = LocalState(Asset) # Asset
        self.local_application = LocalState(Application) # Application
        self.local_account = LocalState(Account) # Account

        ## Global storage
        self.global_int_full = GlobalState(UInt64(50)) # UInt64 with default value = 50
        self.global_int_simplified = UInt64(10) # UInt64 simplified with default value = 10
        self.global_int_no_default = GlobalState(UInt64) # UInt64 with no default value

        self.global_bytes_full = GlobalState(Bytes(b"Hello")) # Bytes with default value = bytes(Hello)
        self.global_bytes_simplified = Bytes(b"Hello") # Bytes simplified with default value = bytes(Hello)
        self.global_bytes_no_default = GlobalState(Bytes) # Bytes with no default value

        self.global_bool_full = GlobalState(True) # Bool
        self.global_bool_simplified = True # Bool
        self.global_bool_no_default = GlobalState(bool) # Bool

        self.global_asset = GlobalState(Asset(UInt64(10))) # Asset
        self.global_application = GlobalState(Application(UInt64(10))) # Application
        # self.global_account = GlobalState(Account(Bytes(b"Hello"))) # Account

        ## Box storage
        self.box_int = Box(UInt64)
        self.box_dynamic_bytes = Box[arc4.DynamicBytes](arc4.DynamicBytes, key="b")
        self.box_string = Box(arc4.String, key=b"BOX_C")
        self.box_bytes = Box(Bytes)
        self.box_map = BoxMap(UInt64, String, key_prefix="") # Box map with uint as key and string as value
        self.box_ref = BoxRef() # Box reference
        self.box_map_struct = BoxMap(arc4.UInt64, UserStruct, key_prefix="users")
        

    ## Local
    @arc4.abimethod
    def contains_local_data(self, for_account: Account) -> bool:       
        assert for_account in self.local_int # Uint64        
        return True
    
    @arc4.abimethod
    def contains_local_data_example(self, for_account: Account) -> bool:       
        assert for_account in self.local_int # Uint64        
        assert for_account in self.local_bytes # Bytes
        assert for_account in self.local_bool # Bool

        assert for_account in self.local_asset # Asset
        assert for_account in self.local_application # Application
        assert for_account in self.local_account # Account
        return True
    
    # delete
    @arc4.abimethod
    def delete_local_data(self, for_account: Account) -> None:
        del self.local_account[for_account] # Uint64
    
    @arc4.abimethod
    def delete_local_data_example(self, for_account: Account) -> bool:
        del self.local_account[for_account] # Uint64

        del self.local_account[for_account] # Bytes
        
        del self.local_account[for_account] # Bool
        
        del self.local_account[for_account] # Asset
        
        del self.local_account[for_account] # Application
        
        del self.local_account[for_account] # Account
        return True

    # get item
    @arc4.abimethod
    def get_item_local_data(self, for_account: Account)-> UInt64:
        return self.local_int[for_account]

    @arc4.abimethod
    def get_item_local_data_example(self, for_account: Account) -> bool:
        assert self.local_int[for_account] == UInt64(10) # Uint64 - returns guranteed data
        assert self.local_bytes[for_account] == b"Hello" # Bytes
        assert self.local_bool[for_account] == True # Bool
        assert self.local_asset[for_account] == Asset(UInt64(10)) # Asset
        assert self.local_application[for_account] == Application(UInt64(10)) # Application
        assert self.local_account[for_account] == Account(Bytes(b"Hello")) # Account
        return True
    
    # set item
    @arc4.abimethod
    def set_local_int(self, for_account: Account, value:  UInt64) -> None:
        self.local_int[for_account] = value # Uint64
    
    @arc4.abimethod
    def set_local_data_example(self, for_account: Account, value_byte: Bytes, value_bool: bool, value_asset: Asset, value_account: Account, value_appln: Application) -> bool:
        self.local_bytes[for_account] = value_byte # Bytes
        assert self.local_bytes[for_account] == value_byte

        self.local_bool[for_account] = value_bool # Bool
        assert self.local_bool[for_account] == value_bool
       
        self.local_asset[for_account] = value_asset # Asset
        assert self.local_asset[for_account] == value_asset

        self.local_application[for_account] = value_appln # Application
        assert self.local_application[for_account] == value_appln

        self.local_account[for_account] = value_account # Account
        assert self.local_account[for_account] == value_account
        return True

    # get function
    @arc4.abimethod
    def get_local_data_with_default_int(self, for_account: Account) -> UInt64:
        return self.local_int.get(for_account, default=UInt64(0)) # Uint64

    @arc4.abimethod
    def get_local_data_with_default(self, for_account: Account) -> bool:
        assert self.local_int.get(for_account, default=UInt64(0)) == UInt64(10) # Uint64
        assert self.local_bytes.get(for_account, default=Bytes(b"Default Value")) == Bytes(b"Hello")  # Bytes
        assert self.local_bool.get(for_account, default=False) == True # Bool
        
        assert self.local_asset.get(for_account, default=Asset(UInt64(0))) == Asset(UInt64(10)) # Asset     
        assert self.local_application.get(for_account, default=Application(UInt64(0))) == Application(UInt64(10)) # Application
        assert self.local_account.get(for_account, default=Account(Bytes(b"Default Value"))) == Account(Bytes(b"Hello")) # Account
        
        return True

    # maybe 
    @arc4.abimethod
    def maybe_local_data(self, for_account: Account) -> tuple[UInt64, bool]:
        # used to get data or assert int
        result, exists = self.local_int.maybe(for_account) # Uint64 
        if not exists:
            result = UInt64(0)
        return result, exists

    @arc4.abimethod
    def maybe_local_data_example(self, for_account: Account) -> bool:
        result, exists = self.local_int.maybe(for_account) # Uint64
        assert exists, "no data for account"
        assert result == UInt64(10)

        resultBytes, exists = self.local_bytes.maybe(for_account) # Bytes
        assert exists, "no data for account"
        assert resultBytes == b"Hello"

        resultBool, exists = self.local_bool.maybe(for_account) # Bool
        assert exists, "no data for account"
        assert resultBool == True

        resultAsset, exists = self.local_asset.maybe(for_account) # Asset
        assert exists, "no data for account"
        assert resultAsset == Asset(UInt64(10))

        resultAppln, exists = self.local_application.maybe(for_account) # Application
        assert exists, "no data for account"
        assert resultAppln == Application(UInt64(10))
        
        resultAccount, exists = self.local_account.maybe(for_account) # Account
        assert exists, "no data for account"
        assert resultAccount == Account(Bytes(b"Hello"))
        return True

    ## Global
    ### get function
    @arc4.abimethod
    def get_global_state(self) -> UInt64:
        return self.global_int_full.get(default=UInt64(0))

    @arc4.abimethod
    def get_global_state_example(self) -> bool:
        assert self.global_int_full.get(default=UInt64(0)) == 50 # uint64
        assert self.global_int_simplified == UInt64(10) # get function cannot be used
        assert self.global_int_no_default.get(default=UInt64(0)) == 0

        assert self.global_bytes_full.get(Bytes(b"default")) == b"Hello" # byte
        return True
    
    ## maybe function
    @arc4.abimethod
    def maybe_global_state(self) -> tuple[UInt64, bool]:
        int_value, int_exists = self.global_int_full.maybe() # uint64
        if not int_exists:
            int_value = UInt64(0)
        return int_value, int_exists

    @arc4.abimethod
    def maybe_global_state_example(self) -> bool:
        int_value, i_exists = self.global_int_full.maybe() # uint64
        assert i_exists
        assert int_value == UInt64(50)
        
        byte_value, b_exists = self.global_bytes_full.maybe() # byte
        assert b_exists
        assert byte_value == b"Hello"

        del self.global_bytes_full.value
        byte_del_value, b_exists = self.global_bytes_full.maybe()
        assert not b_exists
        
        bool_value, i_exists = self.global_bool_full.maybe() # bool
        assert i_exists
        assert bool_value == True

        asset_value, i_exists = self.global_asset.maybe() # Asset
        assert i_exists
        assert asset_value == Asset(UInt64(10))
        
        appln_value, i_exists = self.global_application.maybe() # Application
        assert i_exists
        assert appln_value == Application(UInt64(10))

        return True

    ### value property
    @arc4.abimethod
    def check_global_state_example(self) -> bool:
        assert self.global_int_full.value == 50 # uint64
        # assert self.global_bytes_full.value #== Bytes(b"Hello") # byte
        assert self.global_bool_full.value == True # bool
        
        assert self.global_int_simplified == 10 # uint64
        assert self.global_bytes_simplified == b"Hello" #byte
        assert self.global_bool_simplified == True
        
        assert not self.global_int_no_default
        assert not self.global_bytes_no_default
        assert not self.global_bool_no_default
        
        assert self.global_asset.value == Asset(UInt64(10)) # Asset
        assert self.global_application.value == Application(UInt64(10)) # Application
        # assert self.global_account.value ==  Account(Bytes(b"Hello")) # Account
        return True
    
    ## Box
    ### Bool
    @arc4.abimethod
    def box_exist(self) -> bool:
        return bool(self.box_int)

    @arc4.abimethod
    def box_exist_example(self) -> tuple[bool, bool, bool]:
        return bool(self.box_dynamic_bytes), bool(self.box_string), bool(self.box_bytes)
    
    ### Property key
    @arc4.abimethod
    def key_box(self) -> Bytes:
        return self.box_int.key

    @arc4.abimethod
    def key_box_example(self) -> None:
        assert self.box_dynamic_bytes.key == b"b", "box dynamic bytes key ok"
        assert self.box_string.key == b"BOX_STRING", "box string key ok"
        assert self.box_bytes.key == b"BOX_BYTES", "box bytes key ok"

    ### Get
    @arc4.abimethod
    def get_box(self) -> UInt64:
        return self.box_int.value
    
    @arc4.abimethod
    def get_box_example(self) -> tuple[UInt64, Bytes, arc4.String]:
        return self.box_int.value, self.box_dynamic_bytes.value.native, self.box_string.value
    
    ### Set
    @arc4.abimethod
    def set_box(self, value_int: UInt64) -> None:
        self.box_int.value = value_int

    @arc4.abimethod
    def set_box_example(self, value_int: UInt64, value_dbytes: arc4.DynamicBytes, value_string: arc4.String) -> None:
        self.box_int.value = value_int
        self.box_dynamic_bytes.value = value_dbytes.copy()
        self.box_string.value = value_string
        self.box_bytes.value = value_dbytes.native

        byte_value = self.box_dynamic_bytes.value.copy()
        assert self.box_dynamic_bytes.value.length == byte_value.length, "direct reference should match copy"

        self.box_int.value += 3
    
    ### Maybe
    @arc4.abimethod
    def maybe_box(self) -> tuple[UInt64, bool]:
        box_int_value, box_int_exists = self.box_int.maybe()
        return box_int_value, box_int_exists

    @arc4.abimethod
    def maybe_box_example(self) -> None:
        del self.box_int.value
        assert self.box_int.get(default=UInt64(42)) == 42
        box_int_value, box_int_exists = self.box_int.maybe()
        assert not box_int_exists
        assert box_int_value == 0

    ### Property value
    @arc4.abimethod
    def value_box(self) -> None:
        assert self.box_int.value == UInt64(10)

    ### Property length - fails if box doesn't exist: unrecognised member of algopy.Box

    ### Delete box
    @arc4.abimethod
    def delete_boxes(self) -> None:
        del self.box_int.value
        del self.box_dynamic_bytes.value
        del self.box_string.value
        
        assert self.box_int.get(default=UInt64(42)) == 42
        assert self.box_dynamic_bytes.get(default=arc4.DynamicBytes(b"42")).native == b"42"
        assert self.box_string.get(default=arc4.String("42")) == "42"

    ### Slice box
    @arc4.abimethod
    def slice_box(self) -> None:
        box_0 = Box(Bytes, key=String("0"))
        box_0.value = Bytes(b"Testing testing 123")
        assert box_0.value[0:7] == b"Testing"

        self.box_string.value = arc4.String("Hello")
        assert self.box_string.value.bytes[2:10] == b"Hello"

    @arc4.abimethod
    def arc4_box(self) -> None:
        box_bytes = Box(StaticInts, key=Bytes(b"d"))
        box_bytes.value = StaticInts(arc4.UInt8(0), arc4.UInt8(1), arc4.UInt8(2), arc4.UInt8(3))

        assert box_bytes.value[0] == 0
        assert box_bytes.value[1] == 1
        assert box_bytes.value[2] == 2
        assert box_bytes.value[3] == 3

    ## Box Reference: Property - key


    ### Box Reference: create
    @arc4.abimethod
    def create_box_ref(self) -> None:
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        assert box_ref.create(size=32)
        assert box_ref, "has data"

    ### Box Reference: delete
    @arc4.abimethod
    def test_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # instance box ref
        self.box_ref.create(size=UInt64(32))
        assert self.box_ref, "has data"
        self.box_ref.delete()

    ### Box Reference: extract
    @arc4.abimethod
    def extract_box_ref(self) -> None:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)

        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)
        box_ref.replace(64, value_3)
        prefix = box_ref.extract(0, 32 * 2 + value_3.length)
        assert prefix == app_address + sender_bytes + value_3

    ### Box Reference: resize - not implemented
    @arc4.abimethod
    def key_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)
        box_ref.replace(64, value_3)
        prefix = box_ref.extract(0, 32 * 2 + value_3.length)
        assert prefix == app_address + sender_bytes + value_3

        # delete
        assert box_ref.delete()
        assert box_ref.key == b"blob"

    ### Box Reference: replace
    @arc4.abimethod
    def replace_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)

    ### Box Reference: splice
    @arc4.abimethod
    def splice_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)

    ### Box Reference: get
    @arc4.abimethod
    def get_box_ref(self) -> None:
        # init ref, with valid key types
        box_ref = BoxRef(key="blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=b"blob")
        assert not box_ref, "no data"
        box_ref = BoxRef(key=Bytes(b"blob"))
        assert not box_ref, "no data"
        box_ref = BoxRef(key=String("blob"))
        assert not box_ref, "no data"

        # create
        assert box_ref.create(size=32)
        assert box_ref, "has data"

        # manipulate data
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes
        value_3 = Bytes(b"hello")
        box_ref.replace(0, sender_bytes)
        # box_ref.resize(8000) - not implemented
        box_ref.splice(0, 0, app_address)
        box_ref.replace(64, value_3)
        prefix = box_ref.extract(0, 32 * 2 + value_3.length)
        assert prefix == app_address + sender_bytes + value_3

        # delete
        assert box_ref.delete()
        assert box_ref.key == b"blob"

        # query
        value, exists = box_ref.maybe()
        assert not exists
        assert value == b""
        assert box_ref.get(default=sender_bytes) == sender_bytes

    ### Box Reference: put
    @arc4.abimethod
    def put_box_ref(self) -> None:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)
        
        sender_bytes = Txn.sender.bytes
        app_address = Global.current_application_address.bytes

        assert box_ref.delete()
        assert box_ref.key == b"blob"

        box_ref.put(sender_bytes + app_address)
        assert box_ref, "Blob exists"
        assert box_ref.length == 64

    ### Box Reference: maybe
    @arc4.abimethod
    def maybe_box_ref(self) -> tuple[Bytes, bool]:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)

        value, exists = box_ref.maybe()
        if not exists:
            value = Bytes(b"")
        return value, exists

    ### Box Reference: Property - length 
    @arc4.abimethod
    def length_box_ref(self) -> UInt64:
        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)
        return box_ref.length

    @arc4.abimethod
    def length_box_ref_example(self) -> None:
        box_ref = BoxRef(key="blob")
        assert box_ref.create(size=32)
        assert box_ref.length == 64

        box_ref = BoxRef(key=b"blob")
        assert box_ref.create(size=32)
        assert box_ref.length == 64

        box_ref = BoxRef(key=Bytes(b"blob"))
        assert box_ref.create(size=32)
        assert box_ref.length == 64

        box_ref = BoxRef(key=String("blob"))
        assert box_ref.create(size=32)
        assert box_ref.length == 64
        
    ### Box Map: key prefix
    @arc4.abimethod
    def key_prefix_box_map(self) -> Bytes:
        return self.box_map.key_prefix

    @arc4.abimethod
    def key_prefix_box_map_example(self) -> None:
        assert self.box_map.key_prefix == b""

    ### Box Map: get item
    @arc4.abimethod
    def box_map_get_item(self, key: UInt64) -> String:
        return self.box_map[key]
    
    ### Box Map: set item
    @arc4.abimethod
    def box_map_set(self, key: UInt64, value: String) -> None:
        self.box_map[key] = value

    ### Box Map: del item
    @arc4.abimethod
    def box_map_del(self, key: UInt64) -> None:
        del self.box_map[key]

    ### Box Map: contains
    @arc4.abimethod
    def box_map_exists(self, key: UInt64) -> bool:
        return key in self.box_map
    
    ### Box Map: get
    @arc4.abimethod
    def box_map_get(self) -> String:
        key_1 = UInt64(1)
        return self.box_map.get(key_1, default=String("default"))

    @arc4.abimethod
    def box_map_get_example(self) -> bool:
        key_1 = UInt64(1)
        assert self.box_map.get(key_1, default=String("default")) == String("default")
        return True

    ### Box Map: maybe
    @arc4.abimethod
    def maybe_box_map(self) -> tuple[String, bool]:
        key_1 = UInt64(1)
        value, exists = self.box_map.maybe(key_1)
        if not exists:
            value = String('')
        return value, exists
    
    @arc4.abimethod
    def maybe_box_map_example(self) -> None:
        key_0 = UInt64(0)
        key_1 = UInt64(1)
        value, exists = self.box_map.maybe(key_1)
        assert not exists
        assert key_0 in self.box_map

    ### Box Map: length
    @arc4.abimethod
    def box_map_length(self) -> UInt64:
        # fails if doesnt exist
        key_0 = UInt64(0)
        if not self.box_map:
            return UInt64(0)
        return self.box_map.length(key_0)

    @arc4.abimethod
    def box_map_length_example(self) -> None:
        key_0 = UInt64(0)
        value = String("Hmmmmm")
        self.box_map[key_0] = value
        assert self.box_map[key_0].bytes.length == value.bytes.length
        assert self.box_map.length(key_0) == value.bytes.length

    @arc4.abimethod
    def box_map_struct_length(self) -> bool:
        key_0 = arc4.UInt64(0)
        key_1 = UInt64(1)
        value = UserStruct(
            arc4.String('testName'),
            arc4.UInt64(70),
            arc4.UInt64(2)
        )

        self.box_map_struct[key_0] = value.copy()
        assert self.box_map_struct[key_0].bytes.length == value.bytes.length
        assert self.box_map_struct.length(key_0) == value.bytes.length
        return True
    
    @arc4.abimethod
    def box_map_struct_set(self, key: arc4.UInt64, value: UserStruct) -> bool:
        self.box_map_struct[key]= value.copy()
        assert self.box_map_struct[key] == value
        return True

    @arc4.abimethod
    def box_map_struct_get(self, key: arc4.UInt64) -> UserStruct:
        return self.box_map_struct[key]

    @arc4.abimethod
    def box_map_struct_exists(self, key: arc4.UInt64) -> bool:
        return key in self.box_map_struct
