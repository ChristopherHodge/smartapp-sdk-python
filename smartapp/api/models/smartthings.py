from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Extra, Field, conint, constr


class SmartThings(BaseModel):
    __root__: Any


class Link(BaseModel):
    href: Optional[str] = Field(
        None,
        description='An absolute URL linking to a resource.',
        example='https://...',
    )


class Links(BaseModel):
    next: Optional[Link] = None
    previous: Optional[Link] = None


class Error(BaseModel):
    code: Optional[str] = Field(
        None,
        description='Machine-readable error code.',
        example='ConstraintViolationError',
    )
    message: Optional[str] = Field(
        None,
        description='Human-readable error message.',
        example='The request was malformed.',
    )
    target: Optional[str] = Field(
        None,
        description='Optional field used to point to a problamatic part of the request.',
        example='31192dc9-eb45-4d90-b606-21e9b66d8c2b',
    )
    details: Optional[List[Error]] = None


class OwnerType(Enum):
    USER = 'USER'
    SYSTEM = 'SYSTEM'
    IMPLICIT = 'IMPLICIT'
    ACCOUNT = 'ACCOUNT'


class Owner(BaseModel):
    ownerType: OwnerType = Field(
        ...,
        description='The type of owner that owns this entity. "Account" refers specifically to a coterie account ID.',
    )
    ownerId: str = Field(..., description='A global idenfifier for owner.')


class Tags(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class CapabilityReference(BaseModel):
    id: str = Field(..., example='switch')
    version: Optional[int] = Field(None, example=1)


class CategoryType(Enum):
    manufacturer = 'manufacturer'
    user = 'user'


class DeviceCategory(BaseModel):
    name: str = Field(..., example='Light')
    categoryType: CategoryType


class DeviceCommand(BaseModel):
    component: Optional[str] = Field(
        'main',
        description="The name of the component on this device, default is 'main'. The component must be valid for the device.",
    )
    capability: str = Field(
        ...,
        description='Capability that this command relates to. This must be a capability of the component.',
    )
    command: str = Field(
        ..., description='Name of the command, this must be valid for the capability.'
    )
    arguments: Optional[List[Any]] = Field(
        None,
        description="Arguments of the command.\nAll the required arguments defined in the capability's command argument definition must be provided.\nThe type of the arguments are dependent on the type of the capability's command argument.\nPlease refer to the capabilities definition at https://smartthings.developer.samsung.com/develop/api-ref/capabilities.html\n",
    )


class State(Enum):
    ONLINE = 'ONLINE'
    OFFLINE = 'OFFLINE'


class HealthState(BaseModel):
    state: Optional[State] = Field(None, description='Current state of the device')
    lastUpdatedDate: Optional[datetime] = Field(
        None, description='Last reported date/time in UTC'
    )


class ComponentStatus(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class CapabilityStatus(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class AttributeState(BaseModel):
    value: Optional[Dict[str, Any]] = Field(None, example=0)
    unit: Optional[str] = Field(None, example='°C')
    data: Optional[Dict[str, Dict[str, Any]]] = Field(
        None,
        example={
            'method': 'manual',
            'codeId': 1234,
            'timeout': '2018-05-09T23:03:31+0000',
        },
    )
    timestamp: Optional[datetime] = Field(
        None,
        description='Will always be 0 timezone offset',
        example='2017-12-18T22:14:52.714Z',
    )


class DeviceStateEvent(BaseModel):
    component: Optional[str] = Field(
        None, description="The name of the component on this device, default is 'main'."
    )
    capability: Optional[str] = Field(
        None, description='Capability that this event relates to.'
    )
    attribute: Optional[str] = Field(
        None, description='Name of the capability attribute that this event relates to.'
    )
    value: Any = Field(
        ...,
        description='Value associated with the event. The valid value depends on the capability.',
    )
    unit: Optional[str] = Field(None, description='Unit of the value field.')
    data: Optional[Dict[str, Dict[str, Any]]] = Field(
        None,
        description='Key value pairs about the state of the device. Valid values depend on the capability.',
    )


class App(BaseModel):
    profileId: str = Field(
        ...,
        description='The device profile Id',
        example='6f5ea629-4c05-4a90-a244-cc129b0a80c3',
    )
    installedAppId: str = Field(
        ...,
        description='The ID of the installed application',
        example='6f5ea629-4c05-4a90-a244-cc129b0a80c3',
    )
    externalId: Optional[constr(max_length=64)] = Field(
        None,
        description='A field to store an ID from a system external to SmartThings.',
        example='Th13390',
    )


class DeviceInstallRequest(BaseModel):
    label: Optional[str] = Field(
        None, description='The label for the Device.', example='Living room light'
    )
    locationId: str = Field(
        ...,
        description='The ID of the Location with which the device is associated.',
        example='0c0b935d-0616-4441-a0bf-da7aeec3dc0a',
    )
    roomId: Optional[str] = Field(
        None,
        description='The ID of the Room with which to associate the Device is associated.\nThe Room must be valid for the Location of the Device.\n',
        example='0fd2b1ef-1b33-4a54-9153-65aca91e9660',
    )
    app: App


class FunctionCodes(BaseModel):
    class Config:
        extra = Extra.allow

    default: Optional[str] = None


class IrDeviceDetails(BaseModel):
    parentDeviceId: Optional[str] = Field(
        None, description='The id of the Parent device.'
    )
    profileId: Optional[str] = Field(
        None,
        description='The id of the profile that describes the device components and capabilities.',
        example='0c0b875r-0213-6479-a0bf-da7aeec3dc0a',
    )
    ocfDeviceType: Optional[str] = Field(
        None, description='The OCF Device Type', example='oic.d.tv'
    )
    irCode: Optional[str] = Field(
        None, description='The id of the ircode', example='006C'
    )
    functionCodes: Optional[FunctionCodes] = Field(
        None,
        description='List of IR function codes',
        example={
            'statelessPowerToggleButton.powerToggle': 'power',
            'statelessAudioMuteButton.muteToggle': 'mute',
            'statelessAudioVolumeButton.volumeUp': 'volume_up',
            'statelessAudioVolumeButton.volumeDown': 'volume_down',
            'statelessChannelButton.channelUp': 'channel_up',
            'statelessChannelButton.channelDown': 'channel_down',
            'statelessCustomButton.green': 'green',
            'statelessCustomButton.right': 'right',
            'statelessCustomButton.3': 3,
            'statelessCustomButton.exit': 'exit',
            'statelessCustomButton.playback': 'playback',
        },
    )
    childDevices: Optional[List[IrDeviceDetails]] = Field(
        None, description='list of child devices'
    )
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description='Key value pairs stored in the conductor for the device.\nUI Metadata information\n',
    )


class BleDeviceDetails(BaseModel):
    pass

    class Config:
        extra = Extra.forbid


class BleD2DDeviceDetails(BaseModel):
    encryptionKey: Optional[str] = Field(
        None,
        description='Security encryption key.',
        example='96012869B606355A1F843B1E19DC31B1',
    )
    cipher: Optional[str] = Field(
        None, description='Key for the decrypt.', example='BMO_256-CBS-PKMS1Padding'
    )
    advertisingId: Optional[str] = Field(
        None, description='BLE Advertising Id.', example='9C0D4219'
    )
    identifier: Optional[str] = Field(
        None, description='Unique device identifier.', example='88-57-1d-0e-53-ab'
    )
    configurationVersion: Optional[str] = None
    configurationUrl: Optional[str] = Field(
        None,
        example='https://apisa.samsungiots.com/v1/miniature/profile/e524ceba-93b9-499d-a90a-24214f7f01cb',
    )
    metadata: Optional[Dict[str, Any]] = None


class ViperDeviceDetails(BaseModel):
    uniqueIdentifier: Optional[str] = Field(None, example='1a-74')
    manufacturerName: Optional[str] = Field(None, example='TP-Link')
    modelName: Optional[str] = Field(None, example='HS101')
    swVersion: Optional[str] = Field(None, example='23.123.231')
    hwVersion: Optional[str] = Field(None, example='v1 US bulb')


class OcfDeviceDetails(BaseModel):
    deviceId: Optional[str] = Field(None, description='ID of the device')
    ocfDeviceType: Optional[str] = Field(None, description='OCF device type')
    name: Optional[str] = Field(None, description='Name of the device')
    specVersion: Optional[str] = Field(None, description='OCF spec version')
    verticalDomainSpecVersion: Optional[str] = Field(
        None, description='OCF vertical domain spec version'
    )
    manufacturerName: Optional[str] = Field(None, description='OCF manufacturer name')
    modelNumber: Optional[str] = Field(None, description='OCF model number')
    platformVersion: Optional[str] = Field(None, description='OCF platform version')
    platformOS: Optional[str] = Field(None, description='OCF platform OS')
    hwVersion: Optional[str] = Field(None, description='OCF platform H/W version')
    firmwareVersion: Optional[str] = Field(None, description='OCF firmware version')
    vendorId: Optional[str] = Field(None, description='OCF vendor ID')
    vendorResourceClientServerVersion: Optional[str] = Field(
        None, description='OCF vendor resource client/server version'
    )
    locale: Optional[str] = Field(None, description='Language code')
    lastSignupTime: Optional[str] = Field(
        None, description='The time when the device is signed up lastly'
    )


class DeviceProfileReference(BaseModel):
    id: Optional[str] = Field(
        None,
        description='The device profile Id',
        example='a7b3c264-2d22-416e-bca1-ca4b59a60aee',
    )


class DeviceIntegrationType(Enum):
    BLE = 'BLE'
    BLE_D2D = 'BLE_D2D'
    DTH = 'DTH'
    ENDPOINT_APP = 'ENDPOINT_APP'
    HUB = 'HUB'
    IR = 'IR'
    IR_OCF = 'IR_OCF'
    MQTT = 'MQTT'
    OCF = 'OCF'
    PENGYOU = 'PENGYOU'
    VIDEO = 'VIDEO'
    VIPER = 'VIPER'
    WATCH = 'WATCH'
    GROUP = 'GROUP'
    LAN = 'LAN'
    ZIGBEE = 'ZIGBEE'
    ZWAVE = 'ZWAVE'
    MATTER = 'MATTER'


class CreateDeviceEventsResponse(BaseModel):
    pass


class CommandStatus(Enum):
    ACCEPTED = 'ACCEPTED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'


class DeleteDeviceCommandsResponse(BaseModel):
    pass


class UpdateDeviceComponent(BaseModel):
    id: str = Field(..., example='main')
    icon: Optional[constr(min_length=1, max_length=255)] = Field(
        None,
        description='Identifier allowing the user to pick a custom icon for the device component.\nThe icon of the main component represents the device itself\n',
    )
    categories: List[str] = Field(
        ...,
        description='A case-sensitive string from the pre-defined list of valid categories [/devicecategories](#/operation/listCategories). Allows the user to redefine the category of the device from what the manufacturer set by default.',
        max_items=1,
        min_items=1,
    )


class UpdateDeviceRequest(BaseModel):
    label: Optional[constr(min_length=1, max_length=255)] = Field(
        None, description='The label for the Device.', example='Living room light'
    )
    locationId: Optional[str] = Field(
        None,
        description='The ID of the Location where the Device should be moved to.\nNot all Devices support Location moves.\nMoving between some Locations may be rejected depending on the data region used.\n',
        example='0c0b935d-0616-4441-a0bf-da7aeec3dc0a',
    )
    roomId: Optional[str] = Field(
        None,
        description='The ID of the Room with which to associate the Device is associated.\nThe Room must be valid for the Location of the Device.\n',
        example='0fd2b1ef-1b33-4a54-9153-65aca91e9660',
    )
    components: Optional[List[UpdateDeviceComponent]] = None


class DeviceNetworkSecurityLevel(Enum):
    UNKNOWN = 'UNKNOWN'
    ZWAVE_LEGACY_NON_SECURE = 'ZWAVE_LEGACY_NON_SECURE'
    ZWAVE_S0_LEGACY = 'ZWAVE_S0_LEGACY'
    ZWAVE_S0_FALLBACK = 'ZWAVE_S0_FALLBACK'
    ZWAVE_S2_UNAUTHENTICATED = 'ZWAVE_S2_UNAUTHENTICATED'
    ZWAVE_S2_AUTHENTICATED = 'ZWAVE_S2_AUTHENTICATED'
    ZWAVE_S2_ACCESS_CONTROL = 'ZWAVE_S2_ACCESS_CONTROL'
    ZWAVE_S2_FAILED = 'ZWAVE_S2_FAILED'
    ZWAVE_S0_FAILED = 'ZWAVE_S0_FAILED'
    ZWAVE_S2_DOWNGRADE = 'ZWAVE_S2_DOWNGRADE'
    ZWAVE_S0_DOWNGRADE = 'ZWAVE_S0_DOWNGRADE'


class ExecutingLocally(BaseModel):
    __root__: bool = Field(
        ..., description='True if the device is executing locally on the hub'
    )


class DeviceEui(BaseModel):
    __root__: str = Field(
        ..., description='The EUID of the Zigbee device', example='24FD5B000105DB96'
    )


class DeviceNetworkId(BaseModel):
    __root__: str = Field(
        ..., description='The network-specific identifier of the device on the network'
    )


class DeviceId(BaseModel):
    __root__: str = Field(
        ...,
        description='The identifier for the Device instance.',
        example='6f5ea629-4c05-4a90-a244-cc129b0a80c3',
    )


class DeviceNetworkType(BaseModel):
    __root__: str = Field(..., description='The device network type.', example='ZIGBEE')


class DriverId(BaseModel):
    __root__: str = Field(
        ...,
        description='The ID of the Sprocket driver',
        example='9314a926-528c-403f-ae56-4b0d059381dd',
    )


class HubId(BaseModel):
    __root__: str = Field(
        ...,
        description='The hub that the device is connected to.',
        example='f7239728-edb3-48e9-b588-a27f30b968a0',
    )


class ProvisioningState(Enum):
    PROVISIONED = 'PROVISIONED'
    TYPED = 'TYPED'
    DRIVER_SWITCH = 'DRIVER_SWITCH'
    NONFUNCTIONAL = 'NONFUNCTIONAL'


class Restriction(BaseModel):
    tier: int = Field(
        ...,
        description='The restriction level of an entity to limit actions it can take.',
    )
    historyRetentionTTLDays: Optional[int] = Field(
        None, description='The number of days to retain the state before deletion.'
    )
    visibleWhenRestricted: Optional[bool] = Field(
        False,
        description='Indicate whether or not the entity is visible when restricted.',
    )


class BaseCapabilityReference(BaseModel):
    id: str = Field(..., example='switch')
    version: Optional[int] = Field(None, example=1)


class DeviceProfileMetadata(BaseModel):
    class Config:
        extra = Extra.allow

    __root__: Any = Field(
        ...,
        description='Additional information about the device profile, limited to 10 entries.',
        example={
            'firmWareVersion': '0.2.123',
            'manufacturerName': 'SmartThingsCommunity',
        },
    )


class DeleteDeviceProfileResponse(BaseModel):
    pass


class DeviceProfileStatus(Enum):
    DEVELOPMENT = 'DEVELOPMENT'
    PUBLISHED = 'PUBLISHED'


class LocaleTag(BaseModel):
    __root__: str = Field(
        ...,
        description='The tag of the locale as defined in [RFC bcp47](http://www.rfc-editor.org/rfc/bcp/bcp47.txt).',
        example='en',
    )


class ComponentTranslations(BaseModel):
    label: Optional[constr(max_length=25)] = Field(
        None,
        description='Short UTF-8 text used when displaying the component.',
        example='Main',
    )
    description: Optional[constr(max_length=255)] = Field(
        None,
        description='UTF-8 text describing the component.',
        example='The main component of the device.',
    )


class StringType(Enum):
    text = 'text'
    password = 'password'
    paragraph = 'paragraph'


class Definition(BaseModel):
    minimum: Optional[float] = Field(
        None,
        description='Minimum value a preference may be set to. Only valid for `integer` and `number` preference types.',
    )
    maximum: Optional[float] = Field(
        None,
        description='Maximum value a preference may be set to. Only valid for `integer` and `number` preference types.',
    )
    minLength: Optional[int] = Field(
        None,
        description='Minimum length a string may be set to. Only valid for `string` preference type.',
    )
    maxLength: Optional[int] = Field(
        None,
        description='Maximum length a string may be set to. Only valid for `string` preference type.',
    )
    default: Optional[Any] = Field(None, description='Default value for a preference.')
    stringType: Optional[StringType] = Field(
        None,
        description='The type of a string preference. `text` is a normal preference, `password` encrypts the values, and `paragraph` is for documentation purposes.',
    )
    options: Optional[Dict[str, str]] = Field(
        None, description='The available selections for an `enumeration` preference.'
    )


class PreferenceType(Enum):
    integer = 'integer'
    number = 'number'
    boolean = 'boolean'
    string = 'string'
    enumeration = 'enumeration'


class SmartAppEventRequest(BaseModel):
    name: Optional[str] = Field(
        None,
        description='An arbitrary name for the custom SmartApp event.  Typically useful as a hook for in-app routing.',
    )
    attributes: Optional[Dict[str, str]] = Field(
        None,
        description='An arbitrary set of key / value pairs useful for passing any custom metadata.\n\n* Supports a maximum of 10 entries.\n* Maximum key length: 36 Unicode characters in UTF-8\n* Maximum value length: 256 Unicode characters in UTF-8\n* Allowed characters for *keys* are letters, plus the following special characters: `:`, `_`\n* Allowed characters for *values* are letters, whitespace, and numbers, plus the following special characters: `+`, `-`, `=`, `.`, `_`, `:`, `/`\n* If you need characters outside this allowed set, you can apply standard base-64 encoding.\n',
    )


class DashboardCardLifecycle(Enum):
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


class DeviceGroupType(Enum):
    UNDETERMINED = 'UNDETERMINED'
    GENERIC = 'GENERIC'
    VIDEO_CAMERA = 'VIDEO_CAMERA'
    LIGHTING = 'LIGHTING'


class DeviceGroupCapability(BaseModel):
    id: str = Field(..., example='switch')
    version: Optional[int] = Field(None, example=1)


class Component(BaseModel):
    class Config:
        extra = Extra.allow

    id: Optional[str] = Field(None, example='main')


class Device1(BaseModel):
    deviceId: Optional[str] = Field(
        None,
        description='GUID representing the device',
        example='30d3691f-2416-4cbc-b193-2329581f29d1',
    )
    components: Optional[List[Component]] = Field(
        None, description='Components to add to the group'
    )


class DeviceGroupResponse(BaseModel):
    groupName: str = Field(
        ..., description='Name of the group created', example='helloWorldGroup'
    )
    groupType: DeviceGroupType
    locationId: Optional[str] = Field(
        None,
        description='Location where this group is',
        example='30d3691f-2416-4cbc-b193-2329581f29d1',
    )
    restrictionTier: Optional[int] = Field(
        None, description='restriction tier of the device group'
    )
    devices: List[Device1] = Field(..., description='An array of devices in the group')
    deviceGroupId: str = Field(
        ...,
        description='a GUID that identifies a group',
        example='30d3691f-2416-4cbc-b193-2329581f29d1',
    )
    deviceGroupCapabilities: List[DeviceGroupCapability] = Field(
        ...,
        description='Lowest common denominator capability of all the devices in the group',
    )
    roomId: Optional[str] = None


class DeviceGroupCommand(BaseModel):
    capability: Optional[str] = None
    command: Optional[str] = None
    arguments: Optional[List[Dict[str, Any]]] = None


class UpdateLocationRequest(BaseModel):
    name: constr(min_length=1, max_length=40) = Field(
        ..., description='A name for the Location.'
    )
    latitude: Optional[float] = Field(None, description='A geographical latitude.')
    longitude: Optional[float] = Field(None, description='A geographical longitude.')
    regionRadius: Optional[int] = Field(
        None,
        description='The radius in meters around latitude and longitude which defines this :ocation.',
    )
    temperatureScale: Optional[str] = Field(
        None,
        description='The desired temperature scale used for the Location. Values include F and C.',
    )
    locale: Optional[str] = Field(
        None,
        description='We expect a POSIX locale but we also accept an IETF BCP 47 language tag.',
        example='en_US',
    )
    additionalProperties: Optional[Dict[str, str]] = Field(
        None,
        description='Additional information about the Location that allows SmartThings to further define your Location.',
    )


class DeleteLocationResponse(BaseModel):
    pass


class LocationParentTypes(Enum):
    LOCATIONGROUP = 'LOCATIONGROUP'
    ACCOUNT = 'ACCOUNT'


class Room(BaseModel):
    roomId: Optional[UUID] = Field(None, description='The ID of the room.')
    locationId: Optional[UUID] = Field(
        None, description='The ID of the parent Location.'
    )
    name: Optional[str] = Field(
        None, description='A name for the room (e.g. Living Room)'
    )
    backgroundImage: Optional[str] = Field(None, description='Not currently in use.')
    created: Optional[datetime] = Field(
        None, description='The timestamp of when a room was created in UTC.'
    )
    lastModified: Optional[datetime] = Field(
        None, description='The timestamp of when a room was last updated in UTC.'
    )


class CreateRoomRequest(BaseModel):
    name: constr(min_length=1, max_length=40) = Field(
        ..., description='A name for the room (e.g. Living Room)'
    )


class UpdateRoomRequest(BaseModel):
    name: constr(min_length=1, max_length=40) = Field(
        ..., description='A name for the room.'
    )


class DeleteRoomResponse(BaseModel):
    pass


class Mode(BaseModel):
    id: str = Field(
        ...,
        description='Globally unique id for the mode.',
        example='9206ea57-2e2e-414c-a792-9087117ca3d8',
    )
    label: constr(min_length=1, max_length=25) = Field(
        ...,
        description='A name provided by the User. Unique per Location, updatable.',
        example='Our House',
    )
    name: str = Field(
        ...,
        description='A name provided when the mode was created. The name is unique per Location, and can not be updated.',
        example='Home',
    )


class EntityTypes(Enum):
    LOCATION = 'LOCATION'


class DeliveryType(Enum):
    EMAIL = 'EMAIL'
    LOGINID = 'LOGINID'


class StatusTypes(Enum):
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'


class Ui(BaseModel):
    pluginId: Optional[str] = None
    pluginUri: Optional[AnyUrl] = None
    dashboardCardsEnabled: bool
    preInstallDashboardCardsEnabled: bool


class IconImage(BaseModel):
    url: Optional[AnyUrl] = Field(
        None, description='A default icon image url for an app. https url required.\n'
    )


class Classification(Enum):
    AUTOMATION = 'AUTOMATION'
    SERVICE = 'SERVICE'
    DEVICE = 'DEVICE'
    CONNECTED_SERVICE = 'CONNECTED_SERVICE'
    HIDDEN = 'HIDDEN'
    LABS = 'LABS'


class PrincipalType(Enum):
    LOCATION = 'LOCATION'
    USER_LEVEL = 'USER_LEVEL'


class StringConfig(BaseModel):
    value: Optional[constr(max_length=2048)] = Field(None, description='A config value')


class DeviceConfig(BaseModel):
    deviceId: Optional[str] = Field(None, description='The ID of the device.')
    componentId: Optional[str] = Field(
        None, description='The component ID on the device.'
    )
    permissions: Optional[List[str]] = Field(None, max_items=25)


class PermissionConfig(BaseModel):
    permissions: Optional[List[str]] = Field(None, max_items=25, min_items=1)


class ModeConfig(BaseModel):
    modeId: Optional[str] = Field(None, description='The ID of the mode.')


class SceneConfig(BaseModel):
    sceneId: Optional[str] = Field(None, description='The ID of the scene.')
    permissions: Optional[List[str]] = Field(None, max_items=25)


class MessageConfig(BaseModel):
    messageGroupKey: Optional[str] = Field(
        None, description='The key value of the message group.'
    )


class ValueType(Enum):
    STRING = 'STRING'
    DEVICE = 'DEVICE'
    PERMISSION = 'PERMISSION'
    MODE = 'MODE'
    SCENE = 'SCENE'
    MESSAGE = 'MESSAGE'
    ENUM = 'ENUM'


class ConfigEntry(BaseModel):
    valueType: Optional[ValueType] = Field(None, description='The value type.')
    stringConfig: Optional[StringConfig] = Field(
        None, description='The config if valueType is STRING, meaningless otherwise'
    )
    deviceConfig: Optional[DeviceConfig] = Field(
        None, description='The config if valueType is DEVICE, meaningless otherwise'
    )
    permissionConfig: Optional[PermissionConfig] = Field(
        None, description='The config if valueType is PERMISSION, meaningless otherwise'
    )
    modeConfig: Optional[ModeConfig] = Field(
        None, description='The config if valueType is MODE, meaningless otherwise'
    )
    sceneConfig: Optional[SceneConfig] = Field(
        None, description='The config if valueType is SCENE, meaningless otherwise'
    )
    messageConfig: Optional[MessageConfig] = Field(
        None, description='The config if valueType is MESSAGE, meaningless otherwise'
    )


class ConfigEntries(BaseModel):
    __root__: List[ConfigEntry] = Field(
        ..., description='A list of available configuration values.'
    )


class ConfigMap(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class InstalledAppType(Enum):
    LAMBDA_SMART_APP = 'LAMBDA_SMART_APP'
    WEBHOOK_SMART_APP = 'WEBHOOK_SMART_APP'


class InstallConfigurationStatus(Enum):
    STAGED = 'STAGED'
    DONE = 'DONE'
    AUTHORIZED = 'AUTHORIZED'
    REVOKED = 'REVOKED'


class InstalledAppStatus(Enum):
    PENDING = 'PENDING'
    AUTHORIZED = 'AUTHORIZED'
    REVOKED = 'REVOKED'
    DISABLED = 'DISABLED'


class DeleteInstalledAppResponse(BaseModel):
    count: Optional[int] = None


class CreateInstalledAppEventsResponse(BaseModel):
    pass


class NoticeCode(Enum):
    USER_PAUSE = 'USER_PAUSE'
    REVISIT = 'REVISIT'
    RECONFIGURE = 'RECONFIGURE'


class NoticeAction(Enum):
    DISMISS = 'DISMISS'
    EDIT = 'EDIT'
    NONE = 'NONE'


class OnceSchedule(BaseModel):
    time: int = Field(
        ...,
        description='The time in millis from jan 1 1970 UTC for ONCE schedules. Must be less than 2 years from now.',
    )
    overwrite: Optional[bool] = None


class CronSchedule(BaseModel):
    expression: constr(max_length=256) = Field(
        ...,
        description='The cron expression for the schedule for CRON schedules.\nThe format matches that specified by the [Quartz scheduler](http://www.quartz-scheduler.org/documentation/quartz-2.x/tutorials/crontrigger.html) but should not include the seconds (1st)\nfield. The exact second will be chosen at random but will remain consistent. The years part must be les than 2 years from now.\n',
        example='15 10 * * ? *',
    )
    timezone: str = Field(
        ..., description='The timezone id for CRON schedules.', example='GMT'
    )


class ScheduleRequest(BaseModel):
    once: Optional[OnceSchedule] = None
    name: constr(min_length=1, max_length=36) = Field(
        ...,
        description='The unique per installed app name of the schedule.',
        example='on_schedule-1',
    )
    cron: Optional[CronSchedule] = None


class Schedule(BaseModel):
    installedAppId: Optional[UUID] = Field(
        None,
        description='The ID of the installed app.',
        example='736e3903-001c-4d40-b408-ff40d162a06b',
    )
    locationId: Optional[UUID] = Field(
        None,
        description='The ID of the location the installed app is in.',
        example='35451c7a-cc23-4838-8a3b-1205090cf161',
    )
    userUuid: Optional[UUID] = Field(
        None,
        description='The UUID of the user who created the schedule.',
        example='27843aec-56a1-4b91-83b6-7957d26a3f7d',
    )
    scheduledExecutions: Optional[List[int]] = Field(
        None,
        description='list of scheduled execution times in millis from jan 1 1970 UTC',
    )
    name: constr(min_length=1, max_length=36) = Field(
        ...,
        description='The unique per installed app name of the schedule.',
        example='on_schedule-1',
    )
    cron: Optional[CronSchedule] = None


class PagedSchedules(BaseModel):
    items: Optional[List[Schedule]] = None
    _links: Optional[Links] = None


class DeleteScheduleResponse(BaseModel):
    pass


class SubscriptionSource(Enum):
    DEVICE = 'DEVICE'
    CAPABILITY = 'CAPABILITY'
    MODE = 'MODE'
    DEVICE_LIFECYCLE = 'DEVICE_LIFECYCLE'
    DEVICE_HEALTH = 'DEVICE_HEALTH'
    SECURITY_ARM_STATE = 'SECURITY_ARM_STATE'
    HUB_HEALTH = 'HUB_HEALTH'
    SCENE_LIFECYCLE = 'SCENE_LIFECYCLE'


class DeviceSubscriptionDetail(BaseModel):
    deviceId: str = Field(
        ...,
        description='The GUID of the device that is subscribed to.',
        example='35451c7a-cc23-4838-8a3b-1205090cf161',
    )
    componentId: Optional[str] = Field(
        '*',
        description='The component ID on the device that is subscribed to or * for all.',
        example='main',
    )
    capability: Optional[constr(min_length=1, max_length=128)] = Field(
        '*',
        description='Name of the capability that is subscribed to or * for all.',
        example='switch',
    )
    attribute: Optional[constr(min_length=1, max_length=256)] = Field(
        '*',
        description='Name of the capabilities attribute or * for all.',
        example='switch',
    )
    value: Optional[str] = Field(
        '*',
        description='A particular value for the attribute that will trigger the subscription or * for all.',
        example=['*', 1, 'on', {'key': 30}],
    )
    stateChangeOnly: Optional[bool] = Field(
        None,
        description='Only execute the subscription if the subscribed event is a state change from previous events.',
    )
    subscriptionName: Optional[str] = Field(
        None,
        description='A name for the subscription that will be passed to the installed app. Must be unique per installed app.',
    )
    modes: Optional[List[str]] = Field(
        None,
        description="List of mode ID's that the subscription will execute for. If not provided then all modes will be supported.",
    )


class CapabilitySubscriptionDetail(BaseModel):
    locationId: str = Field(
        ...,
        description='The id of the location that both the app and source device are in.',
    )
    capability: constr(min_length=1, max_length=128) = Field(
        ...,
        description='Name of the capability that is subscribed to.',
        example='switch',
    )
    attribute: Optional[constr(min_length=1, max_length=256)] = Field(
        '*',
        description='Name of the capabilities attribute or * for all.',
        example='switch',
    )
    value: Optional[str] = Field(
        '*',
        description='A particular value for the attribute that will trigger the subscription or * for all.',
        example=['*', 1, 'on', {'key': 30}],
    )
    stateChangeOnly: Optional[bool] = Field(
        True,
        description='Only execute the subscription if the subscribed event is a state change from previous events.',
    )
    subscriptionName: Optional[str] = Field(
        None,
        description='A name for the subscription that will be passed to the installed app. Must be unique per installed app.',
    )
    modes: Optional[List[str]] = Field(
        None,
        description='List of modes that the subscription will execute for. If not provided then all modes will be supported.',
    )


class SubscriptionDelete(BaseModel):
    count: Optional[int] = None


class ModeSubscriptionDetail(BaseModel):
    locationId: str = Field(
        ...,
        description='The GUID for the location to subscribe to mode changes.',
        example='9f24edfd-f2e5-4a82-8a24-c1955ee46419',
    )


class DeviceLifecycleDetail(BaseModel):
    deviceIds: Optional[List[str]] = Field(
        None,
        description='An array of GUIDs of devices being subscribed to. A max of 20 GUIDs are allowed.',
        max_items=20,
    )
    subscriptionName: Optional[str] = Field(
        None,
        description='A name for the subscription that will be passed to the installed app.',
    )
    locationId: Optional[str] = Field(
        None,
        description='The id of the location that both the app and source device are in.',
    )


class DeviceHealthDetail(BaseModel):
    deviceIds: Optional[List[str]] = Field(
        None,
        description='An array of GUIDs of devices being subscribed to. A max of 20 GUIDs are allowed.',
        max_items=20,
    )
    subscriptionName: Optional[str] = Field(
        None,
        description='A name for the subscription that will be passed to the installed app.',
    )
    locationId: Optional[str] = Field(
        None,
        description='The id of the location that both the app and source device are in.',
    )


class SecurityArmStateDetail(BaseModel):
    subscriptionName: Optional[str] = Field(
        None,
        description='A name for the subscription that will be passed to the installed app.',
    )
    locationId: str = Field(
        ...,
        description='The id of the location that both the app and the security system are in.',
    )


class HubHealthDetail(BaseModel):
    subscriptionName: Optional[str] = Field(
        None,
        description='A name for the subscription that will be passed to the installed app.',
    )
    locationId: str = Field(
        ..., description='The id of the location that both the app and hubs are in'
    )


class SceneLifecycleDetail(BaseModel):
    subscriptionName: Optional[str] = Field(
        None,
        description='A name for the subscription that will be passed to the installed app.',
    )
    locationId: str = Field(
        ..., description='The id of the location that both the app and scenes are in.'
    )


class SubscriptionId(BaseModel):
    __root__: UUID = Field(..., description='The subscription id of the subscription.')


class SubscriptionFilterTypes(Enum):
    LOCATIONIDS = 'LOCATIONIDS'
    DEVICEIDS = 'DEVICEIDS'
    INSTALLEDSMARTAPPIDS = 'INSTALLEDSMARTAPPIDS'
    SMARTAPPIDS = 'SMARTAPPIDS'


class SubscriptionFilterValues(BaseModel):
    __root__: List[str] = Field(
        ..., description='An array of subscription filter values.'
    )


class SubscriptionFilterEventTypes(BaseModel):
    __root__: List[str]


class SubscriptionFilterAttributes(BaseModel):
    __root__: List[str]


class SubscriptionFilterCapabilities(BaseModel):
    __root__: List[str]


class SubscriptionFilterComponents(BaseModel):
    __root__: List[str]


class SubscriptionTargetValue(BaseModel):
    __root__: AnyUrl = Field(..., description='The address to send events to.')


class IconImageModel(BaseModel):
    url: Optional[AnyUrl] = Field(
        None, description='A default icon image url for an app. https url required.\n'
    )


class AppType(Enum):
    LAMBDA_SMART_APP = 'LAMBDA_SMART_APP'
    WEBHOOK_SMART_APP = 'WEBHOOK_SMART_APP'


class AppClassification(Enum):
    AUTOMATION = 'AUTOMATION'
    SERVICE = 'SERVICE'
    DEVICE = 'DEVICE'
    CONNECTED_SERVICE = 'CONNECTED_SERVICE'
    HIDDEN = 'HIDDEN'
    LABS = 'LABS'


class AppRegisterRequest(BaseModel):
    pass


class AppRegisterResponse(BaseModel):
    pass


class LambdaSmartApp(BaseModel):
    functions: Optional[List[str]] = Field(
        None, description='A list of AWS arns referencing a Lambda function.'
    )


class AppOAuth(BaseModel):
    clientName: Optional[str] = Field(
        None, description='A name given to the OAuth Client.'
    )
    scope: Optional[List[str]] = Field(
        None,
        description='A list of SmartThings API OAuth scope identifiers that maybe required to execute your integration.',
    )
    redirectUris: Optional[List[AnyUrl]] = Field(
        None, description='A list of redirect URIs.', max_items=10, min_items=0
    )


class CreateOrUpdateLambdaSmartAppRequest(BaseModel):
    functions: List[str] = Field(
        ..., description='A list of AWS arns referencing a Lambda function.'
    )


class CreateOrUpdateWebhookSmartAppRequest(BaseModel):
    targetUrl: str = Field(
        ..., description='A URL that should be invoked during execution.'
    )


class UpdateAppOAuthRequest(BaseModel):
    clientName: str = Field(..., description='A name given to the OAuth Client.')
    scope: List[str] = Field(
        ...,
        description='A list of SmartThings API OAuth scope identifiers that maybe required to execute your integration.',
    )
    redirectUris: List[AnyUrl] = Field(
        ..., description='A list of redirect URIs.', max_items=10, min_items=0
    )


class GenerateAppOAuthRequest(BaseModel):
    clientName: Optional[str] = Field(
        None, description='A name given to the OAuth Client.'
    )
    scope: Optional[List[str]] = Field(
        None,
        description='A list of SmartThings API OAuth scope identifiers that maybe required to execute your integration.',
    )


class DeleteAppResponse(BaseModel):
    pass


class UpdateAppSettingsRequest(BaseModel):
    settings: Optional[Dict[str, str]] = None


class UpdateAppSettingsResponse(BaseModel):
    settings: Optional[Dict[str, str]] = None


class UpdateSignatureTypeResponse(BaseModel):
    pass


class GetAppSettingsResponse(BaseModel):
    settings: Optional[Dict[str, str]] = None


class GenerateAppOAuthResponse(BaseModel):
    oauthClientDetails: Optional[AppOAuth] = None
    oauthClientId: Optional[UUID] = Field(None, description='The OAuth Client ID.')
    oauthClientSecret: Optional[UUID] = Field(
        None, description='The OAuth Client Secret.'
    )


class SignatureType(Enum):
    APP_RSA = 'APP_RSA'
    ST_PADLOCK = 'ST_PADLOCK'


class PrincipalTypeModel(Enum):
    LOCATION = 'LOCATION'
    USER_LEVEL = 'USER_LEVEL'


class AppUISettings(BaseModel):
    pluginId: Optional[str] = None
    pluginUri: Optional[AnyUrl] = None
    dashboardCardsEnabled: bool
    preInstallDashboardCardsEnabled: bool


class AppTargetStatus(Enum):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'


class AdhocMessageTemplate(BaseModel):
    localeTag: LocaleTag
    variables: Optional[Dict[str, str]] = Field(
        None,
        description='A map<string,string> with the key representing the variable name, and the value representing the verbiage\nto be replaced in template string.\n',
    )
    template: str = Field(
        ...,
        description='A message template string.  Specify variables using the double curly braces convention.\ni.e. "Hello, {{ firstName }}!"\n',
    )


class LocaleVariables(BaseModel):
    localeTag: LocaleTag
    variables: Optional[Dict[str, str]] = Field(
        None,
        description='A map<string,string> with the key representing the variable name, and the value representing the verbiage\nto be replaced in template string.\n',
    )


class MessageTemplate(BaseModel):
    localeTag: LocaleTag
    template: str = Field(
        ...,
        description='A message template string. Specify variables using the double curly braces convention.\ni.e. "Hello, {{ firstName }}!"\n',
    )


class MessageType(Enum):
    PREDEFINED = 'PREDEFINED'
    ADHOC = 'ADHOC'


class PagedMessageTemplate(BaseModel):
    appId: UUID = Field(..., description='A globally unique identifier for an app.')
    messageTemplateKey: str


class PredefinedMessage(BaseModel):
    messageTemplateKey: str
    defaultVariables: Optional[Dict[str, str]] = Field(
        None,
        description='A map<string,string> with the key representing the variable name, and the value representing the verbiage\nto be replaced in template string. `defaultVariables` are only used when there are no matching\n`localeVariables`.\n',
    )
    localeVariables: Optional[List[LocaleVariables]] = Field(
        None, description='Variables to resolve for specific locales.\n'
    )


class Status(Enum):
    Enabled = 'Enabled'
    Disabled = 'Disabled'


class ExecutionLocation(Enum):
    Cloud = 'Cloud'
    Local = 'Local'


class OwnerType1(Enum):
    Location = 'Location'
    User = 'User'


class LocationAction(BaseModel):
    locationId: Optional[str] = Field(
        None,
        description='locationId is required for "User level rule". (It\'s optional for "Location level rule")',
    )
    mode: Optional[str] = None


class MapOperand(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class ExecutionResult(Enum):
    Success = 'Success'
    Failure = 'Failure'
    Ignored = 'Ignored'


class IfExecutionResult(Enum):
    True_ = 'True'
    False_ = 'False'


class CommandExecutionResult(Enum):
    Success = 'Success'
    Failure = 'Failure'
    Offline = 'Offline'


class IfActionExecutionResult(BaseModel):
    result: IfExecutionResult


class CommandActionExecutionResult(BaseModel):
    result: CommandExecutionResult
    deviceId: str = Field(..., description='Device ID for device actions')


class LocationActionExecutionResult(BaseModel):
    result: ExecutionResult
    locationId: str = Field(..., description='Location ID for location actions')


class SleepActionExecutionResult(BaseModel):
    result: ExecutionResult


class ActionExecutionResult(BaseModel):
    actionId: str
    if_: Optional[IfActionExecutionResult] = Field(None, alias='if')
    location: Optional[LocationActionExecutionResult] = None
    command: Optional[List[CommandActionExecutionResult]] = None
    sleep: Optional[SleepActionExecutionResult] = None


class RuleExecutionResponse(BaseModel):
    executionId: str
    id: str
    result: ExecutionResult
    actions: Optional[List[ActionExecutionResult]] = None


class LocationAttribute(Enum):
    FineDust = 'FineDust'
    FineDustIndex = 'FineDustIndex'
    Humidity = 'Humidity'
    Mode = 'Mode'
    Security = 'Security'
    Temperature = 'Temperature'
    TemperatureC = 'TemperatureC'
    TemperatureF = 'TemperatureF'
    UltraFineDust = 'UltraFineDust'
    UltraFineDustIndex = 'UltraFineDustIndex'
    Weather = 'Weather'
    WeatherAlertSeverity = 'WeatherAlertSeverity'


class ArmState(Enum):
    ArmedStay = 'ArmedStay'
    ArmedAway = 'ArmedAway'
    Disarmed = 'Disarmed'


class DayOfWeek(Enum):
    Sun = 'Sun'
    Mon = 'Mon'
    Tue = 'Tue'
    Wed = 'Wed'
    Thu = 'Thu'
    Fri = 'Fri'
    Sat = 'Sat'


class DateReference(Enum):
    Today = 'Today'


class TimeReference(Enum):
    Now = 'Now'
    Midnight = 'Midnight'
    Sunrise = 'Sunrise'
    Noon = 'Noon'
    Sunset = 'Sunset'


class IntervalUnit(Enum):
    Second = 'Second'
    Minute = 'Minute'
    Hour = 'Hour'
    Day = 'Day'
    Week = 'Week'
    Month = 'Month'
    Year = 'Year'


class TriggerMode(Enum):
    Auto = 'Auto'
    Always = 'Always'
    Never = 'Never'


class OperandAggregationMode(Enum):
    None_ = 'None'


class ConditionAggregationMode(Enum):
    Any = 'Any'
    All = 'All'


class Sequence(Enum):
    Serial = 'Serial'
    Parallel = 'Parallel'


class ActionSequence(BaseModel):
    actions: Optional[Sequence] = None


class CommandSequence(BaseModel):
    commands: Optional[Sequence] = None
    devices: Optional[Sequence] = None


class IfActionSequence(BaseModel):
    then: Optional[Sequence] = None
    else_: Optional[Sequence] = Field(None, alias='else')


class Creator(Enum):
    SMARTTHINGS = 'SMARTTHINGS'
    ARB = 'ARB'
    RECIPE = 'RECIPE'
    UNDEFINED = 'UNDEFINED'


class SceneSummary(BaseModel):
    sceneId: Optional[str] = Field(
        None, description='The unique identifier of the Scene'
    )
    sceneName: Optional[str] = Field(
        None, description='The user-defined name of the Scene'
    )
    sceneIcon: Optional[str] = Field(None, description='The name of the icon')
    sceneColor: Optional[str] = Field(None, description='The color of the icon')
    locationId: Optional[str] = Field(None, description='Location of the Scene')
    createdBy: Optional[str] = Field(
        None, description='The unique identifier of the user that created the scene'
    )
    createdDate: Optional[datetime] = Field(
        None, description='The date the scene was created'
    )
    lastUpdatedDate: Optional[datetime] = Field(
        None, description='The date the scene was last updated'
    )
    lastExecutedDate: Optional[datetime] = Field(
        None, description='The date the scene was last executed'
    )
    editable: Optional[bool] = Field(
        None,
        description='Whether or not this scene can be edited by the logged in user using the version of the app that made the request',
    )
    apiVersion: Optional[str] = None


class SceneMode(BaseModel):
    modeId: Optional[str] = Field(None, description='the id of the mode')
    modeName: Optional[str] = Field(None, description='the name of the mode')


class SceneModeRequest(BaseModel):
    modeId: str = Field(..., description='The id of the mode')
    actionId: Optional[str] = Field(
        None,
        description='the id of the action to be created. Optional, sent by Reaver only',
    )
    modeName: Optional[str] = Field(None, description='The name of the mode')


class Security(Enum):
    setArmStay = 'setArmStay'
    setArmAway = 'setArmAway'
    disarm = 'disarm'


class SceneSecurityModeRequest(BaseModel):
    actionId: Optional[str] = Field(
        None,
        description='the id of the action to be created. Optional, sent by Reaver only',
    )
    security: Security = Field(..., description='The id of the security mode')
    arguments: Optional[str] = Field(None, description='Additional query param')


class SceneSleepRequest(BaseModel):
    seconds: int = Field(..., description='Number of seconds to sleep the sequence')


class Status1(Enum):
    proposed = 'proposed'
    live = 'live'
    deprecated = 'deprecated'
    dead = 'dead'


class SceneArgument(BaseModel):
    name: Optional[str] = Field(None, description='the name of the command')
    schema_: Optional[Dict[str, Any]] = Field(
        None, alias='schema', description='the schema of the command'
    )
    value: Optional[Dict[str, Any]] = Field(
        None, description='The value being set for the capability command'
    )


class ScenePagedResult(BaseModel):
    items: Optional[List[SceneSummary]] = None
    _links: Optional[Links] = None


class Status2(Enum):
    success = 'success'


class StandardSuccessResponse(BaseModel):
    status: Optional[Status2] = 'success'


class Status3(Enum):
    proposed = 'proposed'
    live = 'live'
    deprecated = 'deprecated'
    dead = 'dead'


class CapabilitySummary(BaseModel):
    id: str = Field(
        ...,
        description='A URL safe unique identifier for the capability.',
        example='switch',
    )
    version: int = Field(
        ..., description='The version number of the capability.', example=1
    )
    status: Status3 = Field(
        ...,
        description='The status of the capability.\n* __proposed__ - The capability is under a review and refinement process. The capability definition may go through changes, some of which may be breaking.\n* __live__ - The capability has been through review and the definition has been solidified. Live capabilities can no longer be altered.\n* __deprecated__ - The capability is marked for removal and should only be used during a period of migration to allow for existing integrations and automations to continue to work.\n* __dead__ - The usage of a deprecated capability has dropped to a sufficiently low level to warrant removal. The capability definition still exists but can no longer be used by automations or implemented by devices.\n',
    )
    ephemeral: Optional[bool] = Field(False, example=True)


class Status4(Enum):
    proposed = 'proposed'
    live = 'live'
    deprecated = 'deprecated'
    dead = 'dead'


class EnumCommand(BaseModel):
    command: str = Field(
        ..., description='the command that sets this attribute to the associated value'
    )
    value: str = Field(
        ..., description='the value that this command will set the attribute to'
    )


class Type(Enum):
    object = 'object'


class AdditionalProperties(Enum):
    boolean_False = False


class RequiredEnum(Enum):
    value = 'value'
    unit = 'unit'
    data = 'data'


class Value(BaseModel):
    class Config:
        extra = Extra.allow

    type: Optional[str] = Field(None, description="Data type of the attribute's value.")
    enum: Optional[List[str]] = Field(
        None,
        description='Array of possible values or a `minimum:` `maximum:` can be defined for `integer` type.',
    )


class Type1(Enum):
    string = 'string'


class Unit(BaseModel):
    type: Optional[Type1] = Field(
        'string',
        description='Data type for the unit. This is defined by capability schema as a `string`.',
    )
    enum: Optional[List[str]] = Field(
        None,
        description='Array of all possible units for the attribute value.',
        example=['mm', 'in'],
    )
    default: Optional[str] = Field(
        None,
        description='The default unit to be used for the attribute value.',
        example='mm',
    )


class Type2(Enum):
    object = 'object'


class Data(BaseModel):
    type: Type2 = Field(
        ..., description='The data type for the `data` schema is object.'
    )
    additionalProperties: Optional[bool] = Field(
        False,
        description='Indicates if properties not explicitly defined by the schema are allowed. Default is false.',
    )
    required: Optional[List[str]] = Field(
        None, description='An array of the properties the `data` schema requires.'
    )
    properties: Optional[Dict[str, Any]] = Field(
        None,
        description='Objects can be described in JSON schema for the `data` that should be stored on this attribute.',
        example={'val': {'type': 'string'}},
    )


class AttributeProperties(BaseModel):
    class Config:
        extra = Extra.forbid

    value: Value = Field(
        ...,
        description='Properties that describe the value of an attribute.',
        example={'type': 'number', 'minimum': 0, 'maximum': 20},
    )
    unit: Optional[Unit] = Field(
        None, description='The unit which describes the value of the attribute.'
    )
    data: Optional[Data] = Field(
        None,
        description='Special case details may be desired to describe the attribute that may not be used the same as a value. Some examples are a timeout or a lock code.',
    )


class Argument(BaseModel):
    class Config:
        extra = Extra.forbid

    name: constr(regex=r'^[[a-z]*([A-Z][a-z]*)*]{1,36}$') = Field(
        ...,
        description='A name that is unique within the command. Used for i18n and named argument command execution.',
    )
    optional: Optional[bool] = Field(
        False,
        description='Whether or not the argument must be supplied.\nIf the argument is at the end of the arguments array then it can be completely ignored.\nIf the argument is followed by another argument `null` must be supplied.\n',
    )
    schema_: Dict[str, Any] = Field(
        ...,
        alias='schema',
        description='[JSON schema](http://json-schema.org/specification-links.html#draft-4) for the argument. The API implements JSON schema version 4. For more info regarding JSON schema, please read [Understanding JSON Schema](https://json-schema.org/understanding-json-schema/index.html).\n',
    )


class I18n(BaseModel):
    label: str = Field(
        ..., description='The localized substitution for the property value'
    )
    description: Optional[str] = Field(None, description='A description of the value')


class Attributes(BaseModel):
    label: Optional[str] = Field(
        None,
        description='The localized version of the label value',
        example='Modo de ar condicionado',
    )
    description: Optional[str] = Field(
        None,
        description='A localized description of what the attribute represents',
        example='Modo de ar condicionado',
    )
    displayTemplate: Optional[str] = Field(
        None,
        description='A template string for the text that will be displayed regarding the attribute state.',
        example='é suposto {{device.label}} a palavra {{attribute}} igual a {{value}}.',
    )
    i18n: Optional[Dict[str, Dict[str, I18n]]] = Field(
        None,
        description='Map of state property (value, unit, etc..) to localization mapping',
    )


class I18n1(BaseModel):
    label: str = Field(
        ..., description='The localized substitution for the argument value'
    )


class Arguments(BaseModel):
    i18n: Optional[Dict[str, I18n1]] = Field(
        None, description='Map of argument values to localizations'
    )
    label: Optional[str] = None
    description: Optional[str] = None


class Commands(BaseModel):
    label: Optional[str] = None
    description: Optional[str] = None
    arguments: Optional[Dict[str, Arguments]] = Field(
        None, description='Map of argument name to localizations'
    )


class CapabilityLocalization(BaseModel):
    tag: LocaleTag
    label: Optional[str] = Field(
        None,
        description='A localized label for the capability',
        example='Modo de ar condicionado',
    )
    description: Optional[str] = Field(
        None,
        description='A localized description of the capability',
        example='Modo de ar condicionado',
    )
    attributes: Optional[Dict[str, Attributes]] = Field(
        None,
        description='Map of attribute name to localizations',
        example={
            'airConditionerMode': {
                'displayTemplate': 'é suposto {{device.label}} a palavra {{attribute}} igual a {{value}}.',
                'label': 'Este é o modo de ar condicionado',
                'i18n': {
                    'value': {
                        'auto': {
                            'label': 'Auto',
                            'description': 'Este é o modo automático',
                        },
                        'cool': {'label': 'Frio', 'description': 'Este é o modo frio'},
                    }
                },
            }
        },
    )
    commands: Optional[Dict[str, Commands]] = Field(
        None,
        description='Map of command name to localizations',
        example={
            'setAirConditionerMode': {
                'arguments': {
                    'mode': {
                        'i18n': {'auto': {'label': 'Auto'}, 'cool': {'label': 'Frio'}}
                    }
                }
            }
        },
    )


class DeleteNamespaceResponse(BaseModel):
    pass


class OwnerType2(Enum):
    user = 'user'
    organization = 'organization'
    system = 'system'


class Namespace(BaseModel):
    name: str = Field(
        ...,
        description='A URL safe globally unique namespace name (ascii letters and numbers only)',
        example='companyx',
    )
    ownerType: OwnerType2 = Field(
        ..., description='The type of owner of the namespace.'
    )
    ownerId: str = Field(
        ...,
        description='id of the owner (user, or in the future, organization)',
        example='0c0b935d-0616-4441-a0bf-da7aeec3dc0a',
    )


class DeviceActivity(BaseModel):
    deviceId: Optional[str] = Field(None, description='Device ID')
    deviceName: Optional[str] = Field(
        None, description='Device nick name', example='TV'
    )
    locationId: Optional[str] = Field(None, description='Location ID')
    locationName: Optional[str] = Field(
        None, description='Location name', example='Home'
    )
    time: Optional[datetime] = Field(
        None,
        description='The IS0-8601 date time strings in UTC of the activity',
        example='2017-12-18T22:14:52Z',
    )
    text: Optional[str] = Field(
        None,
        description='Translated human readable string (localized)',
        example='battery of Button is: 89%',
    )
    component: str = Field(
        ..., description='device component ID. Not nullable.', example='main'
    )
    componentLabel: Optional[str] = Field(
        None, description='device component label. Nullable.', example='left button'
    )
    capability: Optional[str] = Field(
        None, description='capability name', example='battery'
    )
    attribute: Optional[str] = Field(
        None, description='attribute name', example='battery'
    )
    value: Optional[Dict[str, Any]] = Field(
        None, description='attribute value', example=0
    )
    unit: Optional[str] = Field(None, example='%')
    data: Optional[Dict[str, Dict[str, Any]]] = Field(
        None,
        example={
            'method': 'manual',
            'codeId': 1234,
            'timeout': '2018-05-09T23:03:31+0000',
        },
    )
    translatedAttributeName: Optional[str] = Field(
        None,
        description="translated attribute name based on 'Accept-Language' requested in header",
        example='스위치',
    )
    translatedAttributeValue: Optional[str] = Field(
        None,
        description="translated attribute value based on 'Accept-Language' requested in header",
        example='켜짐',
    )


class Capability1(Enum):
    alert = 'alert'
    weather = 'weather'
    airQuality = 'airQuality'
    forecast = 'forecast'
    airQualityForecast = 'airQualityForecast'


class ServiceSubscriptionBody(BaseModel):
    capabilities: List[Capability1] = Field(
        ...,
        description='capability name(s).\nNOTE: alert cannot be combined with other capabilities\n',
    )
    isaId: str = Field(..., description='InstalledApp ID\n')
    geoplaceId: Optional[str] = Field(
        None,
        description='Geo Place ID (This ID is only supported in "alert" capability)\n',
    )
    type: Optional[str] = Field(
        None, description='DIRECT or EXECUTION delivery, default to DIRECT'
    )
    predicate: Optional[str] = Field(
        None,
        description='JEXL formatted expression. See https://commons.apache.org/proper/commons-jexl/reference/syntax.html\n',
    )


class ServiceNewSubscription(BaseModel):
    locationId: str = Field(..., description='location ID')
    subscriptionId: Optional[str] = Field(None, description='subscription ID created')


class ServiceDeleteSubscription(BaseModel):
    locationId: str = Field(..., description='location ID')
    count: float = Field(..., description='number of subscription deleted')


class ServiceCapability(Enum):
    alert = 'alert'
    weather = 'weather'
    airQuality = 'airQuality'
    forecast = 'forecast'
    airQualityForecast = 'airQualityForecast'


class ServiceCapabilities(BaseModel):
    __root__: List[ServiceCapability] = Field(
        ...,
        description='capability name(s)',
        example={
            'capabilities': [
                'alert',
                'weather',
                'forecast',
                'airQuality',
                'airQualityForecast',
            ]
        },
    )


class LastUpdateTime(BaseModel):
    value: Optional[str] = Field(
        None,
        description='Time the data was pull from content provider.\nISO 8601 in UTC - YYYY-MM-DDTHH:MM:SS.SSSZ\n',
    )


class HeadlineText(BaseModel):
    value: Optional[str] = Field(None, description='severe alert headline text')


class Severity(BaseModel):
    value: Optional[int] = Field(
        None,
        description='severity of the alert. Smaller the number the more severe the alert is.',
    )


class MessageType1(BaseModel):
    value: Optional[int] = Field(None, description='1: new\n2: update\n3: cancel\n')


class IssueTime(BaseModel):
    value: Optional[str] = Field(None, description='UTC time when the alert is issued')


class ExpireTime(BaseModel):
    value: Optional[str] = Field(None, description='UTC time when the alert is expired')


class AlertItem(BaseModel):
    lastUpdateTime: Optional[LastUpdateTime] = None
    headlineText: Optional[HeadlineText] = None
    severity: Optional[Severity] = None
    messageType: Optional[MessageType1] = None
    issueTime: Optional[IssueTime] = None
    expireTime: Optional[ExpireTime] = None


class LastUpdateTime1(BaseModel):
    value: Optional[str] = Field(
        None,
        description='Time the data was pull from content provider.\nISO 8601 in UTC - YYYY-MM-DDTHH:MM:SS.SSSZ\n',
    )


class Vendor(BaseModel):
    value: Optional[str] = Field(None, description='Name of the content provider')


class Version1(BaseModel):
    value: Optional[str] = Field(
        None, description='API version number used with the given vendor'
    )


class AirQualityIndex(BaseModel):
    value: Optional[int] = Field(None, description='air quality index')
    unit: Optional[str] = Field(None, description='CAQI')


class O3Amount(BaseModel):
    value: Optional[float] = Field(
        None, description='(Available for Korea Only) Ozone pollutant in ug/m3'
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class O3Index(BaseModel):
    value: Optional[float] = Field(
        None, description='(Available for non-Korea Only) index of Ozone pollutant'
    )
    unit: Optional[str] = Field(None, description='EPA')


class No2Amount(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(Available for Korea Only) Nitrogen Dioxide pollutant in ug/m3',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class No2Index(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(Available for non-Korea Only) index of Nitrogen Dioxide pollutant',
    )
    unit: Optional[str] = Field(None, description='EPA')


class So2Amount(BaseModel):
    value: Optional[float] = Field(
        None, description='(Available for Korea Only) Sulfur Dioxide pollutant in ug/m3'
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class So2Index(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(Available for non-Korea Only) index of Sulfur Dioxide pollutant',
    )
    unit: Optional[str] = Field(None, description='EPA')


class CoAmount(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(Available for Korea Only) Carbon Monoxide pollutant in ug/m3',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class CoIndex(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(Available for non-Korea Only) index of Carbon Monoxide pollutant',
    )
    unit: Optional[str] = Field(None, description='EPA')


class Pm10Amount(BaseModel):
    value: Optional[float] = Field(
        None, description='amount of particulate matter less than 10 microns in ug/m3'
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Index(BaseModel):
    value: Optional[int] = Field(
        None, description='index of particulate matter less than 10 microns'
    )
    unit: Optional[str] = Field(None, description='EPA')


class Pm25Amount(BaseModel):
    value: Optional[float] = Field(
        None, description='amount of particulate matter less than 2.5 microns in ug/m3'
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Index(BaseModel):
    value: Optional[int] = Field(
        None, description='index of particulate matter less than 2.5 microns'
    )
    unit: Optional[str] = Field(None, description='EPA')


class AirQuality(BaseModel):
    lastUpdateTime: Optional[LastUpdateTime1] = None
    vendor: Optional[Vendor] = None
    version: Optional[Version1] = None
    airQualityIndex: Optional[AirQualityIndex] = None
    o3Amount: Optional[O3Amount] = None
    o3Index: Optional[O3Index] = None
    no2Amount: Optional[No2Amount] = None
    no2Index: Optional[No2Index] = None
    so2Amount: Optional[So2Amount] = None
    so2Index: Optional[So2Index] = None
    coAmount: Optional[CoAmount] = None
    coIndex: Optional[CoIndex] = None
    pm10Amount: Optional[Pm10Amount] = None
    pm10Index: Optional[Pm10Index] = None
    pm25Amount: Optional[Pm25Amount] = None
    pm25Index: Optional[Pm25Index] = None


class LastUpdateTime2(BaseModel):
    value: Optional[str] = Field(
        None,
        description='Time the data was pull from content provider.\nISO 8601 in UTC - YYYY-MM-DDTHH:MM:SS.SSSZ\n',
    )


class Vendor1(BaseModel):
    value: Optional[str] = Field(None, description='Name of the content provider')


class Version2(BaseModel):
    value: Optional[str] = Field(
        None, description='API version number used with the given vendor'
    )


class Precip1Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour liquid precipitation amount in millimeters\n'
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 1 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nmaximium 1 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n2 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 2 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 2 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n3 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 3 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 3 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n4 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 4 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 4 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = None


class Precip5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan) 5 hours forecast liquid precipitation amount in millimeters',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 5 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 5 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='6 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 6 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 6 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n7 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 7 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 7 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n8 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 8 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 8 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n9 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 9 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 9 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n10 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 10 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 10 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n11 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 11 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 11 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n12 hours forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMin12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 12 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class PrecipMax12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nminimium 12 hour forecast liquid precipitation amount in millimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Precip24Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='Rolling twenty-four hour liquid precipitation amount in\nmillimeters\n',
    )
    unit: Optional[str] = Field(None, description='mm')


class Snow1Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='One hour snowfall amount in centimeters\n'
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium one hour forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium one hour forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n2 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 2 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 2 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n3 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 3 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 3 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n4 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 4 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 4 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n5 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 5 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 5 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow6Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='6 hours forecast snowfall amount in centimeters\n'
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 6 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 6 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n7 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 7 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 7 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n8 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 8 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 8 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n9 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 9 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 9 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n10 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 10 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 10 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n11 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 11 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 11 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\n12 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMin12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMinimium 12 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class SnowMax12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea and Japan)\nMaximium 12 hours forecast snowfall amount in centimeters\n',
    )
    unit: Optional[str] = Field(None, description='cm')


class Snow24Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Twenty four hour snowfall amount in centimeters\n'
    )
    unit: Optional[str] = Field(None, description='cm')


class Temperature1Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature2Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature3Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature4Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature5Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature6Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature7Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature8Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature9Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature10Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature11Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Temperature12Hour(BaseModel):
    value: Optional[float] = Field(
        None, description='Rolling hour temperature in Celcius.\n'
    )
    unit: Optional[str] = Field(None, description='C')


class Forecast(BaseModel):
    lastUpdateTime: Optional[LastUpdateTime2] = None
    vendor: Optional[Vendor1] = None
    version: Optional[Version2] = None
    precip1Hour: Optional[Precip1Hour] = None
    precipMin1Hour: Optional[PrecipMin1Hour] = None
    precipMax1Hour: Optional[PrecipMax1Hour] = None
    precip2Hour: Optional[Precip2Hour] = None
    precipMin2Hour: Optional[PrecipMin2Hour] = None
    precipMax2Hour: Optional[PrecipMax2Hour] = None
    precip3Hour: Optional[Precip3Hour] = None
    precipMin3Hour: Optional[PrecipMin3Hour] = None
    precipMax3Hour: Optional[PrecipMax3Hour] = None
    precip4Hour: Optional[Precip4Hour] = None
    precipMin4Hour: Optional[PrecipMin4Hour] = None
    precipMax4Hour: Optional[PrecipMax4Hour] = None
    precip5Hour: Optional[Precip5Hour] = None
    precipMin5Hour: Optional[PrecipMin5Hour] = None
    precipMax5Hour: Optional[PrecipMax5Hour] = None
    precip6Hour: Optional[Precip6Hour] = None
    precipMin6Hour: Optional[PrecipMin6Hour] = None
    precipMax6Hour: Optional[PrecipMax6Hour] = None
    precip7Hour: Optional[Precip7Hour] = None
    precipMin7Hour: Optional[PrecipMin7Hour] = None
    precipMax7Hour: Optional[PrecipMax7Hour] = None
    precip8Hour: Optional[Precip8Hour] = None
    precipMin8Hour: Optional[PrecipMin8Hour] = None
    precipMax8Hour: Optional[PrecipMax8Hour] = None
    precip9Hour: Optional[Precip9Hour] = None
    precipMin9Hour: Optional[PrecipMin9Hour] = None
    precipMax9Hour: Optional[PrecipMax9Hour] = None
    precip10Hour: Optional[Precip10Hour] = None
    precipMin10Hour: Optional[PrecipMin10Hour] = None
    precipMax10Hour: Optional[PrecipMax10Hour] = None
    precip11Hour: Optional[Precip11Hour] = None
    precipMin11Hour: Optional[PrecipMin11Hour] = None
    precipMax11Hour: Optional[PrecipMax11Hour] = None
    precip12Hour: Optional[Precip12Hour] = None
    precipMin12Hour: Optional[PrecipMin12Hour] = None
    precipMax12Hour: Optional[PrecipMax12Hour] = None
    precip24Hour: Optional[Precip24Hour] = None
    snow1Hour: Optional[Snow1Hour] = None
    snowMin1Hour: Optional[SnowMin1Hour] = None
    snowMax1Hour: Optional[SnowMax1Hour] = None
    snow2Hour: Optional[Snow2Hour] = None
    snowMin2Hour: Optional[SnowMin2Hour] = None
    snowMax2Hour: Optional[SnowMax2Hour] = None
    snow3Hour: Optional[Snow3Hour] = None
    snowMin3Hour: Optional[SnowMin3Hour] = None
    snowMax3Hour: Optional[SnowMax3Hour] = None
    snow4Hour: Optional[Snow4Hour] = None
    snowMin4Hour: Optional[SnowMin4Hour] = None
    snowMax4Hour: Optional[SnowMax4Hour] = None
    snow5Hour: Optional[Snow5Hour] = None
    snowMin5Hour: Optional[SnowMin5Hour] = None
    snowMax5Hour: Optional[SnowMax5Hour] = None
    snow6Hour: Optional[Snow6Hour] = None
    snowMin6Hour: Optional[SnowMin6Hour] = None
    snowMax6Hour: Optional[SnowMax6Hour] = None
    snow7Hour: Optional[Snow7Hour] = None
    snowMin7Hour: Optional[SnowMin7Hour] = None
    snowMax7Hour: Optional[SnowMax7Hour] = None
    snow8Hour: Optional[Snow8Hour] = None
    snowMin8Hour: Optional[SnowMin8Hour] = None
    snowMax8Hour: Optional[SnowMax8Hour] = None
    snow9Hour: Optional[Snow9Hour] = None
    snowMin9Hour: Optional[SnowMin9Hour] = None
    snowMax9Hour: Optional[SnowMax9Hour] = None
    snow10Hour: Optional[Snow10Hour] = None
    snowMin10Hour: Optional[SnowMin10Hour] = None
    snowMax10Hour: Optional[SnowMax10Hour] = None
    snow11Hour: Optional[Snow11Hour] = None
    snowMin11Hour: Optional[SnowMin11Hour] = None
    snowMax11Hour: Optional[SnowMax11Hour] = None
    snow12Hour: Optional[Snow12Hour] = None
    snowMin12Hour: Optional[SnowMin12Hour] = None
    snowMax12Hour: Optional[SnowMax12Hour] = None
    snow24Hour: Optional[Snow24Hour] = None
    temperature1Hour: Optional[Temperature1Hour] = None
    temperature2Hour: Optional[Temperature2Hour] = None
    temperature3Hour: Optional[Temperature3Hour] = None
    temperature4Hour: Optional[Temperature4Hour] = None
    temperature5Hour: Optional[Temperature5Hour] = None
    temperature6Hour: Optional[Temperature6Hour] = None
    temperature7Hour: Optional[Temperature7Hour] = None
    temperature8Hour: Optional[Temperature8Hour] = None
    temperature9Hour: Optional[Temperature9Hour] = None
    temperature10Hour: Optional[Temperature10Hour] = None
    temperature11Hour: Optional[Temperature11Hour] = None
    temperature12Hour: Optional[Temperature12Hour] = None


class LastUpdateTime3(BaseModel):
    value: Optional[str] = Field(
        None,
        description='Time the data was pull from content provider.\nISO 8601 in UTC - YYYY-MM-DDTHH:MM:SS.SSSZ\n',
    )


class Vendor2(BaseModel):
    value: Optional[str] = Field(None, description='Name of the content provider')


class Version3(BaseModel):
    value: Optional[str] = Field(
        None, description='API version number used with the given vendor'
    )


class Pm10Index1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\none hour index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n2 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n3 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n4 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n5 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\nsix hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n7 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n8 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n9 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n10 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n11 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Index12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n12 hours index forecast of particulate matter less than 10 microns\n',
    )


class Pm10Amount1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\none hour dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n2 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n3 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n4 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n5 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\nsix hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n7 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n8 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n9 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n10 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n11 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm10Amount12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n12 hours dust amount forecast of particulate matter less than 10 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Index1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\none hour index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n2 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n3 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n4 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n5 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\nsix hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n7 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n8 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n9 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n10 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n11 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Index12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n12 hours index forecast of particulate matter less than 2.5 microns\n',
    )


class Pm25Amount1Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\none hour dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount2Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n2 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount3Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n3 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount4Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n4 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount5Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n5 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount6Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\nsix hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount7Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n7 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount8Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n8 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount9Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n9 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount10Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n10 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount11Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n11 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class Pm25Amount12Hour(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is only available in Korea)\n12 hours dust amount forecast of particulate matter less than 2.5 microns\n',
    )
    unit: Optional[str] = Field(None, description='μg/m^3')


class AirQualityForecast(BaseModel):
    lastUpdateTime: Optional[LastUpdateTime3] = None
    vendor: Optional[Vendor2] = None
    version: Optional[Version3] = None
    pm10Index1Hour: Optional[Pm10Index1Hour] = None
    pm10Index2Hour: Optional[Pm10Index2Hour] = None
    pm10Index3Hour: Optional[Pm10Index3Hour] = None
    pm10Index4Hour: Optional[Pm10Index4Hour] = None
    pm10Index5Hour: Optional[Pm10Index5Hour] = None
    pm10Index6Hour: Optional[Pm10Index6Hour] = None
    pm10Index7Hour: Optional[Pm10Index7Hour] = None
    pm10Index8Hour: Optional[Pm10Index8Hour] = None
    pm10Index9Hour: Optional[Pm10Index9Hour] = None
    pm10Index10Hour: Optional[Pm10Index10Hour] = None
    pm10Index11Hour: Optional[Pm10Index11Hour] = None
    pm10Index12Hour: Optional[Pm10Index12Hour] = None
    pm10Amount1Hour: Optional[Pm10Amount1Hour] = None
    pm10Amount2Hour: Optional[Pm10Amount2Hour] = None
    pm10Amount3Hour: Optional[Pm10Amount3Hour] = None
    pm10Amount4Hour: Optional[Pm10Amount4Hour] = None
    pm10Amount5Hour: Optional[Pm10Amount5Hour] = None
    pm10Amount6Hour: Optional[Pm10Amount6Hour] = None
    pm10Amount7Hour: Optional[Pm10Amount7Hour] = None
    pm10Amount8Hour: Optional[Pm10Amount8Hour] = None
    pm10Amount9Hour: Optional[Pm10Amount9Hour] = None
    pm10Amount10Hour: Optional[Pm10Amount10Hour] = None
    pm10Amount11Hour: Optional[Pm10Amount11Hour] = None
    pm10Amount12Hour: Optional[Pm10Amount12Hour] = None
    pm25Index1Hour: Optional[Pm25Index1Hour] = None
    pm25Index2Hour: Optional[Pm25Index2Hour] = None
    pm25Index3Hour: Optional[Pm25Index3Hour] = None
    pm25Index4Hour: Optional[Pm25Index4Hour] = None
    pm25Index5Hour: Optional[Pm25Index5Hour] = None
    pm25Index6Hour: Optional[Pm25Index6Hour] = None
    pm25Index7Hour: Optional[Pm25Index7Hour] = None
    pm25Index8Hour: Optional[Pm25Index8Hour] = None
    pm25Index9Hour: Optional[Pm25Index9Hour] = None
    pm25Index10Hour: Optional[Pm25Index10Hour] = None
    pm25Index11Hour: Optional[Pm25Index11Hour] = None
    pm25Index12Hour: Optional[Pm25Index12Hour] = None
    pm25Amount1Hour: Optional[Pm25Amount1Hour] = None
    pm25Amount2Hour: Optional[Pm25Amount2Hour] = None
    pm25Amount3Hour: Optional[Pm25Amount3Hour] = None
    pm25Amount4Hour: Optional[Pm25Amount4Hour] = None
    pm25Amount5Hour: Optional[Pm25Amount5Hour] = None
    pm25Amount6Hour: Optional[Pm25Amount6Hour] = None
    pm25Amount7Hour: Optional[Pm25Amount7Hour] = None
    pm25Amount8Hour: Optional[Pm25Amount8Hour] = None
    pm25Amount9Hour: Optional[Pm25Amount9Hour] = None
    pm25Amount10Hour: Optional[Pm25Amount10Hour] = None
    pm25Amount11Hour: Optional[Pm25Amount11Hour] = None
    pm25Amount12Hour: Optional[Pm25Amount12Hour] = None


class LastUpdateTime4(BaseModel):
    value: Optional[str] = Field(
        None,
        description='Time the data was pull from content provider.\nISO 8601 in UTC - YYYY-MM-DDTHH:MM:SS.SSSZ\n',
    )


class Vendor3(BaseModel):
    value: Optional[str] = Field(None, description='Name of the content provider')


class Version4(BaseModel):
    value: Optional[str] = Field(
        None, description='API version number used with the given vendor'
    )


class CloudCeiling(BaseModel):
    value: Optional[float] = Field(
        None,
        description='(This attribute is not available in Korea and Japan) Base of lowest Mostly Cloudy or Cloudy layer in meters\n',
    )
    unit: Optional[str] = Field(None, description='m')


class CloudCoverPhrase(BaseModel):
    value: Optional[str] = Field(
        None,
        description='(This attribute is not available in Korea and Japan)\nDescriptive sky cover - based on percentage of cloud cover.\n\nRange - Clear: coverage < 0.09375; Partly Cloudy: coverage < .59375; Mostly Cloudy: coverage < .75; Cloudy: coverage >= .75\n',
    )


class IconCode(BaseModel):
    value: Optional[int] = Field(
        None, description='This number is the key to the weather icon lookup.'
    )


class ConditionState(BaseModel):
    value: Optional[str] = Field(
        None,
        description='enumerated string of [CLEAR, SNOW, RAIN, CLOUDY, STORM, DUSTY, FOGGY]',
    )


class RelativeHumidity(BaseModel):
    value: Optional[int] = Field(
        None,
        description='The relative humidity of the air, which is defined as the\nratio of the amount of water vapor in the air to the amount\nof vapor required to bring the air to saturation at a\nconstant temperature. Relative humidity is always expressed\nas a percentage.\n\nRange - 0 to 10\n',
    )
    unit: Optional[str] = Field(None, description='%')


class SunriseTimeLocal(BaseModel):
    value: Optional[str] = Field(
        None,
        description='This field contains the local time of sunrise. It reflects\nany local daylight savings conventions in UTC.\n\nISO 8601 in UTC - YYYY-MM-DDTHH:MM:SS.SSSZ\n',
    )


class SunsetTimeLocal(BaseModel):
    value: Optional[str] = Field(
        None,
        description='This field contains the local time of sunset. It reflects\nany local daylight savings conventions.\n\nISO 8601 in UTC - YYYY-MM-DDTHH:MM:SS.SSSZ\n',
    )


class Temperature(BaseModel):
    value: Optional[float] = Field(None, description='Temperature in Celcius\n')
    unit: Optional[str] = Field(None, description='C')


class TemperatureFeelsLike(BaseModel):
    value: Optional[float] = Field(
        None, description='An apparent temperature in Celcius\n'
    )
    unit: Optional[str] = Field(None, description='C')


class UvDescription(BaseModel):
    value: Optional[str] = Field(
        None,
        description='(This attribute is not available in Korea and Japan) The UV index description which complements the uvIndex value\n',
    )
    unit: Optional[str] = None


class UvIndex(BaseModel):
    value: Optional[int] = Field(
        None,
        description='The UV index provides indices of the intensity of the solar\nradiation level and risk of skin damage due to exposure.\n\nRange - -2=Not Available, -1=No Report, 0-2=Low, 3-5=Moderate, 6-7=High, 8-10= Very High, 11-16=Extreme\n',
    )


class Visibility(BaseModel):
    value: Optional[float] = Field(
        None,
        description='The horizontal visibility at the observation point in kilometers\n',
    )
    unit: Optional[str] = Field(None, description='Km')


class WeatherDetailUrl(BaseModel):
    value: Optional[str] = Field(
        None,
        description='A detail URL from weather vendor with a detail weather information web page\n',
    )


class WindDirection(BaseModel):
    value: Optional[float] = Field(
        None,
        description='The magnetic wind direction from which the wind blows\nexpressed in degrees.\n\nRange - 0<=wind_dire_deg<=350, in 10 degree intervals\n',
    )
    unit: Optional[str] = Field(None, description='°')


class WindDirectionCardinal(BaseModel):
    value: Optional[str] = Field(
        None,
        description='(This attribute is not available in Korea and Japan)\nThis field contains the cardinal direction from which the\nwind blows in an abbreviated form.\n\nRange - N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW, CALM\n',
    )


class WindGust(BaseModel):
    value: Optional[float] = Field(
        None,
        description='This data field contains information about sudden and\ntemporary variations of the average Wind Speed in kilometers\nper hour.\n',
    )
    unit: Optional[str] = Field(None, description='Km/h')


class WindSpeed(BaseModel):
    value: Optional[float] = Field(
        None,
        description='The wind information reported in the hourly current\nconditions corresponds to a 10-minute average called the\nsustained wind speed in kilometers per hour\n',
    )
    unit: Optional[str] = Field(None, description='Km/h')


class WxPhraseLong(BaseModel):
    value: Optional[str] = Field(
        None,
        description='A text description of observed weather conditions\naccompanying the iconCode field.\n\nRange - 32 character phrase\n',
    )


class Weather(BaseModel):
    lastUpdateTime: Optional[LastUpdateTime4] = None
    vendor: Optional[Vendor3] = None
    version: Optional[Version4] = None
    cloudCeiling: Optional[CloudCeiling] = None
    cloudCoverPhrase: Optional[CloudCoverPhrase] = None
    iconCode: Optional[IconCode] = None
    conditionState: Optional[ConditionState] = None
    relativeHumidity: Optional[RelativeHumidity] = None
    sunriseTimeLocal: Optional[SunriseTimeLocal] = None
    sunsetTimeLocal: Optional[SunsetTimeLocal] = None
    temperature: Optional[Temperature] = None
    temperatureFeelsLike: Optional[TemperatureFeelsLike] = None
    uvDescription: Optional[UvDescription] = None
    uvIndex: Optional[UvIndex] = None
    visibility: Optional[Visibility] = None
    weatherDetailUrl: Optional[WeatherDetailUrl] = None
    windDirection: Optional[WindDirection] = None
    windDirectionCardinal: Optional[WindDirectionCardinal] = None
    windGust: Optional[WindGust] = None
    windSpeed: Optional[WindSpeed] = None
    wxPhraseLong: Optional[WxPhraseLong] = None


class ServiceCapabilityData(BaseModel):
    locationId: str = Field(..., description='location ID')
    name: Optional[ServiceCapabilities] = None
    alert: Optional[List[AlertItem]] = None
    airQuality: Optional[AirQuality] = None
    forecast: Optional[Forecast] = None
    airQualityForecast: Optional[AirQualityForecast] = None
    weather: Optional[Weather] = None


class AudioFormat(Enum):
    mp3 = 'mp3'
    pcm = 'pcm'


class TtsProvider(Enum):
    polly = 'polly'
    bixby = 'bixby'


class Engine(Enum):
    standard = 'standard'
    neural = 'neural'


class SpeakingStyle(Enum):
    news = 'news'
    conversational = 'conversational'


class TTSBody(BaseModel):
    text: str = Field(
        ...,
        description='Text to be converted to audio. Cannot exceed 2000 characters for Polly and 425 characters for Bixby',
    )
    languageCode: str = Field(
        ...,
        description='Language used for the text to be converted to speech. Please refer tts/info API to get the options available',
    )
    voiceId: str = Field(
        ...,
        description='VoiceId to be used for the text. Please refer tts/info API to get the options available',
    )
    audioFormat: Optional[AudioFormat] = Field(
        None,
        description='Audio format of the audio file, default to mp3 when ttsProvider is Amazon Polly, default to pcm when ttsProvider is Bixby. Amazon Polly supports mp3 and pcm. Bixby supports only pcm.',
    )
    ttsProvider: Optional[TtsProvider] = Field(
        None,
        description='TTS provider to use for converting text to speech, default to polly',
    )
    engine: Optional[Engine] = Field(
        None,
        description='TTS engine to be used, default to standard, standard - robotic voice, neural - human like and natural voice. This option is available only when ttsProvider is Amazon Polly. Please refer tts/info API to get the options available',
    )
    speakingStyle: Optional[SpeakingStyle] = Field(
        None,
        description='Speaking style to be used. This option is available only when ttsProvider is Amazon Polly, engine is neural, and voiceIds are one of the following - Matthew, Joanna, Lupe. Please refer tts/info API to get the options available',
    )


class AudioFormat1(Enum):
    mp3 = 'mp3'
    pcm = 'pcm'


class TtsProvider1(Enum):
    polly = 'polly'
    bixby = 'bixby'


class Engine1(Enum):
    standard = 'standard'
    neural = 'neural'


class SpeakingStyle1(Enum):
    news = 'news'
    conversational = 'conversational'


class PlaytextBody(BaseModel):
    deviceId: str = Field(
        ...,
        description='Device ID of device on which the audio should be played. Device must support audioNotification capability.',
    )
    text: str = Field(
        ...,
        description='Text to be converted to audio. Cannot exceed 2000 characters for Polly and 425 characters for Bixby',
    )
    languageCode: str = Field(
        ...,
        description='Language used for the text to be converted to speech. Please refer tts/info API to get the options available',
    )
    voiceId: str = Field(
        ...,
        description='VoiceId to be used for the text. Please refer tts/info API to get the options available',
    )
    audioFormat: Optional[AudioFormat1] = Field(
        None,
        description='Audio format of the audio file, default to mp3 when ttsProvider is Amazon Polly, default to pcm when ttsProvider is Bixby. Amazon Polly supports mp3 and pcm. Bixby supports only pcm.',
    )
    ttsProvider: Optional[TtsProvider1] = Field(
        None,
        description='TTS provider to use for converting text to speech, default to polly',
    )
    engine: Optional[Engine1] = Field(
        None,
        description='TTS engine to be used, default to standard, standard - robotic voice, neural - human like and natural voice. This option is available only when ttsProvider is Amazon Polly. Please refer tts/info API to get the options available',
    )
    speakingStyle: Optional[SpeakingStyle1] = Field(
        None,
        description='Speaking style to be used. This option is available only when ttsProvider is Amazon Polly, engine is neural, and voiceIds are one of the following - Matthew, Joanna, Lupe. Please refer tts/info API to get the options available',
    )
    volume: Optional[conint(ge=0, le=100)] = Field(
        None,
        description='Volume of the device at which the audio notification will be played',
    )


class ConvertedTTS(BaseModel):
    message: str = Field(..., description='message to indicate success')
    audioURL: str = Field(..., description='Audio URL')


class PlayedText(BaseModel):
    message: str = Field(..., description='message to indicate success')


class Gender(Enum):
    Female = 'Female'
    Male = 'Male'


class SupportedEngine(Enum):
    neural = 'neural'
    standard = 'standard'


class TTSProvider(Enum):
    bixby = 'bixby'
    polly = 'polly'


class SpeakingStyleEnum(Enum):
    news = 'news'
    conversational = 'conversational'


class Voice(BaseModel):
    Gender: Gender = Field(..., description='Gender of the voice')
    Id: str = Field(..., description='Voice id of the voice')
    LanguageCode: str = Field(..., description='Language code of the voice')
    LanguageName: str = Field(..., description='Language of the voice')
    Name: str = Field(..., description='Name of the voice')
    SupportedEngines: Optional[List[SupportedEngine]] = Field(
        None,
        description='Supported engines for the voice. This option will be available only when TTSProvider is Amazon Polly',
    )
    TTSProvider: TTSProvider = Field(..., description='TTS provider for the voice')
    SpeakingStyle: Optional[List[SpeakingStyleEnum]] = Field(
        None,
        description='Supported speaking styles for the voice.  This option will be available only when TTSProvider is Amazon Polly, engine is neural, and voiceIds are one of the following - Matthew, Joanna, Lupe',
    )


class TTSInfo(BaseModel):
    voices: List[Voice] = Field(..., description='Voices supported by the TTS service')


class PartnerSTConnection(Enum):
    connected = 'connected'
    disconnected = 'disconnected'


class PartnerSTConnection1(Enum):
    connected = 'connected'
    disconnected = 'disconnected'


class IsaResults(BaseModel):
    isaId: str = Field(..., description='isaId installed for the user')
    appName: str = Field(
        ...,
        description='SmartThings Schema connector name given by partner eg Lifx (Connect)',
    )
    partnerName: str = Field(..., description='Parnter name eg Lifx Inc')
    icon: str = Field(..., description='url of partner icon')
    icon2x: str = Field(..., description='url of partner icon in 2x dimensions')
    icon3x: str = Field(..., description='url of partner icon in 3x dimensions')
    locationId: str = Field(..., description='location of the installed smart app')
    partnerSTConnection: PartnerSTConnection1 = Field(
        ..., description='connection status between partner and ST platform'
    )
    endpointAppId: str = Field(
        ..., description='endpoint app id of the installed smart app'
    )


class DeviceResults(BaseModel):
    deviceId: Optional[str] = Field(None, description='deviceId created by DM')
    name: Optional[str] = Field(
        None, description='initial device name from the partner'
    )


class CommandArguments(BaseModel):
    __root__: str = Field(..., example=30)


class PostReceipt(BaseModel):
    endpointAppId: Optional[UUID] = Field(
        None, example='viper_9121f970-f503-11e8-a7de-7319cef9605d'
    )
    stClientId: Optional[UUID] = Field(
        None, example='e3fd04cb-c488-4bbd-9759-8deb512656a8'
    )
    stClientSecret: Optional[UUID] = Field(
        None,
        example='02c75d945e69e167233cb635b1f9be76d97ebb0b04f4e6839f3acfad320bed64ab86838dc6312585b037259e7797bf2bb44b3caa7a60539c1f402abe3bbe9256424615fddc48e76823b9c230b15669901becb33711e48192aa54a31e4e287ff47295c61c15e2e046103f13aa250bb561136625b69304cc31ef5004d267d0847184426144c60a74329bb47e2f773469ebb6a1e585175370fda78e03413abbcafe51665e8cbe51adf37dd5a3ff376300ebdbe2a359589951a72867bd3fcc574bd77b9ac85127023f931de3c5bcb213efeab3d94a7ee4a3d20acc6f6e575755b10bceb74290f4182c9bddc407d4361710492611568ebcb0b2ffac09e70d0c977d5f',
    )


class GenerateStOauthBody(BaseModel):
    endpointAppId: Optional[str] = Field(
        None, description='SmartThings Schema App id for the partner'
    )


class ViperAppLinks(BaseModel):
    android: Optional[str] = Field(
        None, description='app deep linking to partners in android'
    )
    ios: Optional[str] = Field(None, description='app deep linking to partners in ios')
    isLinkingEnabled: Optional[bool] = Field(
        None, description='whether deep app linking is enabled'
    )


class EventType(Enum):
    DEVICE_COMMANDS_EVENT = 'DEVICE_COMMANDS_EVENT'
    DEVICE_EVENT = 'DEVICE_EVENT'
    DEVICE_HEALTH_EVENT = 'DEVICE_HEALTH_EVENT'
    DEVICE_LIFECYCLE_EVENT = 'DEVICE_LIFECYCLE_EVENT'
    HUB_HEALTH_EVENT = 'HUB_HEALTH_EVENT'
    MODE_EVENT = 'MODE_EVENT'
    SCENE_LIFECYCLE_EVENT = 'SCENE_LIFECYCLE_EVENT'
    SECURITY_ARM_STATE_EVENT = 'SECURITY_ARM_STATE_EVENT'
    TIMER_EVENT = 'TIMER_EVENT'
    INSTALLED_APP_LIFECYCLE_EVENT = 'INSTALLED_APP_LIFECYCLE_EVENT'
    WEATHER_EVENT = 'WEATHER_EVENT'


class EventOwnerType(Enum):
    LOCATION = 'LOCATION'
    USER = 'USER'


class DeviceEvent(BaseModel):
    eventId: Optional[str] = Field(
        None,
        description='The ID of the event.',
        example='736e3903-001c-4d40-b408-ff40d162a06b',
    )
    locationId: Optional[str] = Field(
        None,
        description='The id of the location in which the event was triggered.\n\nThis field is not used or populated for user-level events.\n\nLocation id may also be sent in `ownerId` with `ownerType` = `LOCATION`.\n',
        example='499e28ba-b33b-49c9-a5a1-cce40e41f8a6',
    )
    ownerId: Optional[str] = Field(
        None,
        description='ID for what owns the device event. Works in tandem with `ownerType` as a composite identifier.',
    )
    ownerType: Optional[EventOwnerType] = None
    deviceId: Optional[str] = Field(
        None,
        description='The ID of the device associated with the DEVICE_EVENT.',
        example='6f5ea629-4c05-4a90-a244-cc129b0a80c3',
    )
    componentId: Optional[str] = Field(
        None,
        description='The name of the component on the device that the event is associated with.',
        example='main',
    )
    capability: Optional[str] = Field(
        None,
        description='The name of the capability associated with the DEVICE_EVENT.',
        example='motionSensor',
    )
    attribute: Optional[str] = Field(
        None,
        description='The name of the DEVICE_EVENT. This typically corresponds to an attribute name of the device-handler’s capabilities.',
        example='motion',
    )
    value: Optional[str] = Field(
        None,
        description="The value of the event. The type of the value is dependent on the capability's attribute type.\n",
        example='active',
    )
    valueType: Optional[str] = Field(
        None,
        description='The root level data type of the value field. The data types are representitive of standard JSON data types.\n',
        example='number',
    )
    unit: Optional[str] = Field(
        None, description='Unit of the value field.', example='°C'
    )
    stateChange: Optional[bool] = Field(
        None,
        description='Whether or not the state of the device has changed as a result of the DEVICE_EVENT.',
    )
    data: Optional[Dict[str, Any]] = Field(
        None, description='json map as defined by capability data schema'
    )
    subscriptionName: Optional[str] = Field(
        None,
        description='The name of subscription that caused delivery.',
        example='motion_sensors',
    )


class ModeEvent(BaseModel):
    eventId: Optional[str] = Field(None, description='The id of the event.')
    locationId: Optional[str] = Field(
        None, description='The id of the location in which the event was triggered.'
    )
    modeId: Optional[str] = Field(
        None, description='The ID of the mode associated with a MODE_EVENT.'
    )


class TimerType(Enum):
    CRON = 'CRON'
    ONCE = 'ONCE'


class DeviceCommandsEventCommand(BaseModel):
    componentId: Optional[str] = Field(None, example='main')
    capability: Optional[str] = Field(None, example='switch')
    command: Optional[str] = Field(None, example='on')
    arguments: Optional[List[Dict[str, Any]]] = Field(None, example=[])


class ArmState1(Enum):
    UNKNOWN = 'UNKNOWN'
    ARMED_STAY = 'ARMED_STAY'
    ARMED_AWAY = 'ARMED_AWAY'
    DISARMED = 'DISARMED'


class Status5(Enum):
    OFFLINE = 'OFFLINE'
    ONLINE = 'ONLINE'
    UNHEALTHY = 'UNHEALTHY'


class Reason(Enum):
    NONE = 'NONE'
    SERVICE_UNAVAILABLE = 'SERVICE_UNAVAILABLE'
    HUB_OFFLINE = 'HUB_OFFLINE'
    ZWAVE_OFFLINE = 'ZWAVE_OFFLINE'
    ZIGBEE_OFFLINE = 'ZIGBEE_OFFLINE'
    BLUETOOTH_OFFLINE = 'BLUETOOTH_OFFLINE'
    HUB_DISCONNECTED = 'HUB_DISCONNECTED'


class Status6(Enum):
    OFFLINE = 'OFFLINE'
    ONLINE = 'ONLINE'
    ZWAVE_OFFLINE = 'ZWAVE_OFFLINE'
    ZWAVE_ONLINE = 'ZWAVE_ONLINE'
    ZIGBEE_OFFLINE = 'ZIGBEE_OFFLINE'
    ZIGBEE_ONLINE = 'ZIGBEE_ONLINE'
    BLUETOOTH_OFFLINE = 'BLUETOOTH_OFFLINE'
    BLUETOOTH_ONLINE = 'BLUETOOTH_ONLINE'


class Reason1(Enum):
    NONE = 'NONE'
    DISCONNECTED = 'DISCONNECTED'
    INACTIVE = 'INACTIVE'


class HubHealthEvent(BaseModel):
    eventId: Optional[str] = Field(None, description='The id of the event.')
    locationId: Optional[str] = Field(
        None, description='The id of the location in which the event was triggered.'
    )
    hubId: Optional[str] = Field(None, description='The id of the hub.')
    status: Optional[Status6] = Field(None, description='The status of the hub.\n')
    reason: Optional[Reason1] = Field(
        None, description='The reason the hub is offline.\n'
    )


class DeviceLifecycle(Enum):
    CREATE = 'CREATE'
    DELETE = 'DELETE'
    UPDATE = 'UPDATE'
    MOVE_FROM = 'MOVE_FROM'
    MOVE_TO = 'MOVE_TO'
    ROOM_MOVE = 'ROOM_MOVE'


class Category(BaseModel):
    name: Optional[str] = None


class DeviceLifecycleCreate(BaseModel):
    presentationId: Optional[str] = None
    manufacturerName: Optional[str] = None
    categories: Optional[List[Category]] = None
    parentDeviceId: Optional[str] = None
    hubId: Optional[str] = None


class DeviceLifecycleDelete(BaseModel):
    pass


class LabelDiff(BaseModel):
    old: Optional[str] = None
    new: Optional[str] = None


class Category1(BaseModel):
    name: Optional[str] = None


class Capability2(BaseModel):
    id: Optional[str] = None
    version: Optional[int] = None


class Old(BaseModel):
    id: Optional[str] = None
    label: Optional[str] = None
    categories: Optional[List[Category1]] = None
    capabilities: Optional[List[Capability2]] = None


class Category2(BaseModel):
    name: Optional[str] = None


class Capability3(BaseModel):
    id: Optional[str] = None
    version: Optional[int] = None


class New(BaseModel):
    id: Optional[str] = None
    label: Optional[str] = None
    categories: Optional[List[Category2]] = None
    capabilities: Optional[List[Capability3]] = None


class ComponentDiff(BaseModel):
    old: Optional[Old] = None
    new: Optional[New] = None


class DeviceLifecycleUpdate(BaseModel):
    labelDiff: Optional[LabelDiff] = None
    componentDiff: Optional[ComponentDiff] = None


class DeviceLifecycleMove(BaseModel):
    locationId: Optional[str] = None


class DeviceLifecycleRoomMove(BaseModel):
    roomIdFrom: Optional[str] = None
    roomIdTo: Optional[str] = None


class ValueType1(Enum):
    NULL_VALUE = 'NULL_VALUE'
    INT_VALUE = 'INT_VALUE'
    DOUBLE_VALUE = 'DOUBLE_VALUE'
    STRING_VALUE = 'STRING_VALUE'
    BOOLEAN_VALUE = 'BOOLEAN_VALUE'


class SimpleValue(BaseModel):
    valueType: Optional[ValueType1] = Field(
        None, description='The type of the value.\n'
    )
    intValue: Optional[int] = None
    doubleValue: Optional[float] = None
    stringValue: Optional[str] = None
    boolValue: Optional[bool] = None


class SceneLifecycle(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    CREATEFORBIXBY = 'CREATEFORBIXBY'
    UPDATEFORBIXBY = 'UPDATEFORBIXBY'
    DELETEFORBIXBY = 'DELETEFORBIXBY'


class SceneLifecycleCreate(BaseModel):
    pass


class SceneLifecycleUpdate(BaseModel):
    pass


class SceneLifecycleDelete(BaseModel):
    pass


class SceneLifecycleCreateForBixby(BaseModel):
    pass


class SceneLifecycleUpdateForBixby(BaseModel):
    pass


class SceneLifecycleDeleteForBixby(BaseModel):
    pass


class InstalledAppLifecycle(Enum):
    CREATE = 'CREATE'
    INSTALL = 'INSTALL'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    OTHER = 'OTHER'


class InstalledAppLifecycleCreate(BaseModel):
    pass


class InstalledAppLifecycleUpdate(BaseModel):
    pass


class InstalledAppLifecycleDelete(BaseModel):
    pass


class InstalledAppLifecycleInstall(BaseModel):
    pass


class InstalledAppLifecycleOther(BaseModel):
    pass


class InstalledAppLifecycleError(BaseModel):
    code: Optional[str] = None
    message: Optional[str] = None
    target: Optional[str] = None
    details: Optional[List[InstalledAppLifecycleError]] = None


class ConditionState1(Enum):
    UNKNOWN = 'UNKNOWN'
    CLEAR = 'CLEAR'
    SNOW = 'SNOW'
    RAIN = 'RAIN'
    CLOUDY = 'CLOUDY'
    STORM = 'STORM'
    DUSTY = 'DUSTY'
    FOGGY = 'FOGGY'


class WeatherData(BaseModel):
    cloudCeilingInM: Optional[int] = Field(None, description='Cloud ceiling in meters')
    cloudCoverPhrase: Optional[str] = Field(
        None, description='The phrase of the cloud cover'
    )
    relativeHumidityInPercent: Optional[int] = Field(
        None, description='Relative Humidity Percentage'
    )
    sunriseDate: Optional[str] = None
    sunsetDate: Optional[str] = None
    temperatureInC: Optional[float] = Field(
        None, description='Temperature in degrees celsius'
    )
    temperatureFeelsLikeInC: Optional[float] = Field(
        None, description='Feels-like temperature in degrees celsius'
    )
    uvDescription: Optional[str] = None
    uvIndex: Optional[int] = None
    visibilityInKm: Optional[float] = None
    windDirectionInDegrees: Optional[int] = None
    windDirectionCardinal: Optional[str] = None
    windGustInKmph: Optional[int] = None
    windSpeedInKmph: Optional[int] = None
    conditionPhraseLong: Optional[str] = None
    conditionState: Optional[ConditionState1] = None


class AirQualityData(BaseModel):
    airQualityIndex: Optional[int] = None
    o3AmountInUgm3: Optional[float] = None
    o3Index: Optional[int] = None
    no2AmountInUgm3: Optional[float] = None
    no2Index: Optional[int] = None
    so2AmountInUgm3: Optional[float] = None
    so2Index: Optional[int] = None
    coAmountInUgm3: Optional[float] = None
    coIndex: Optional[int] = None
    pm10AmountInUgm3: Optional[float] = None
    pm10Index: Optional[int] = None
    pm25AmountInUgm3: Optional[float] = None
    pm25Index: Optional[int] = None


class Severity1(Enum):
    UNKNOWN_SEVERITY = 'UNKNOWN_SEVERITY'
    EXTREME = 'EXTREME'
    SEVERE = 'SEVERE'
    MODERATE = 'MODERATE'


class State1(Enum):
    NONE = 'NONE'
    NEW = 'NEW'
    UPDATE = 'UPDATE'
    CANCEL = 'CANCEL'


class SevereAlertData(BaseModel):
    headlineText: Optional[str] = None
    detailUrl: Optional[str] = None
    startTime: Optional[str] = None
    endTime: Optional[str] = None
    severity: Optional[Severity1] = None
    state: Optional[State1] = None


class WeatherEvent(BaseModel):
    weatherData: Optional[WeatherData] = None
    airQualityData: Optional[AirQualityData] = None
    severeAlertData: Optional[SevereAlertData] = None
    geoPlaceId: Optional[str] = Field(None, description='The id of the GeoPlace.')


class ComponentId(BaseModel):
    component: Optional[str] = Field(
        None,
        description='Human readable identifier for a device component.',
        example='main',
    )


class View(Enum):
    DETAIL_VIEW = 'DETAIL_VIEW'
    DASHBOARD = 'DASHBOARD'
    AUTOMATION_ACTIONS = 'AUTOMATION_ACTIONS'
    AUTOMATION_CONDITIONS = 'AUTOMATION_CONDITIONS'


class DeviceConfigView(BaseModel):
    view: Optional[View] = None


class Type3(Enum):
    dth = 'dth'
    profile = 'profile'


class DeviceConfigType(BaseModel):
    type: Optional[Type3] = 'profile'


class Type4(Enum):
    dth = 'dth'
    profile = 'profile'


class PoCodes(BaseModel):
    label: str
    po: constr(regex=r'^___PO_CODE_[a-zA-Z0-9_]+$') = Field(
        ..., description="Po code. Should begin with '___PO_CODE'"
    )


class Os(Enum):
    android = 'android'
    ios = 'ios'
    tizen = 'tizen'
    web = 'web'


class DpInfoItem(BaseModel):
    os: Os = Field(
        ...,
        description="The OS of the UI Client used to show the details page. 'iOS': iOS SmartThings 'android': Android SmartThings",
    )
    dpUri: str = Field(
        ...,
        description="This is linked to obtain the vendor-specific device details page. The device's dashboard card opens the detail view using this link when the user clicks the device card.",
        example='plugin://example_detail_page_uri',
    )
    operatingMode: Optional[str] = Field(
        None,
        description='This describes operating mode after onboarding. `easySetup` will launch the plugin for setting up your device while `deviceControl` will launch the plugin for controlling the device directly after onboarding.',
    )


class DpInfo(BaseModel):
    __root__: List[DpInfoItem] = Field(
        ...,
        description='Information used for obtaining details page plugins on different platforms. Array of Details page link objects.',
    )


class Type5(Enum):
    inactive = 'inactive'
    active = 'active'


class IconUrl(BaseModel):
    __root__: str = Field(
        ...,
        description='Preloaded iconId or URL used to retrieve icons to be drawn on the UI Client.',
        example='preload://example_icon_url',
    )


class Step(BaseModel):
    __root__: float = Field(
        ...,
        description='The incremental step that increases or decreases for numeric values.',
    )


class Range(BaseModel):
    __root__: List[float] = Field(
        ...,
        description='The inclusive range of a numeric value or bounds of a string depending on the data type it is applied to.',
        example=[0, 100],
        max_items=2,
        min_items=2,
    )


class Operator(Enum):
    CONTAINS = 'CONTAINS'
    DOES_NOT_CONTAIN = 'DOES_NOT_CONTAIN'
    EQUALS = 'EQUALS'
    DOES_NOT_EQUAL = 'DOES_NOT_EQUAL'
    GREATER_THAN = 'GREATER_THAN'
    GREATER_THAN_OR_EQUALS = 'GREATER_THAN_OR_EQUALS'
    LESS_THAN = 'LESS_THAN'
    LESS_THAN_OR_EQUALS = 'LESS_THAN_OR_EQUALS'
    ONE_OF = 'ONE_OF'


class Version(BaseModel):
    __root__: int = Field(
        ..., description='The version number of the capability.', example=1
    )


class Mnmn(BaseModel):
    __root__: str = Field(
        ..., description='The name of the manufacturer', example='SmartThingsCommunity'
    )


class Vid(BaseModel):
    __root__: str = Field(
        ...,
        description="A unique identifier for the presentation of a device. This can be a model number on legacy device integrations, but also may be a system generated UUID based on a device's structure and display configuration.",
        example='MySmartDevice',
    )


class CapabilityKey(BaseModel):
    capability: str
    version: Optional[Version] = None


class Component1(BaseModel):
    __root__: str = Field(..., example='main')


class FormattedLabel(BaseModel):
    __root__: str = Field(
        ...,
        description='This displays a string. This can be a formatted string with variables.\nExample: `{{attribute.value}} {{attribute.unit}}` (where `attribute` is the name of an attribute in your capability)\n',
        example='{{temperatureMeasurement.value}}',
    )


class SupportedValues(BaseModel):
    __root__: constr(regex=r'(^[[a-z]*([A-Z][a-z]*)*){1,36}(\.value)+') = Field(
        ...,
        description='The attribute name specified in supportedValues is an array that has values supported at runtime.',
        example='supportedMode.value',
    )


class DisplayType(Enum):
    pushButton = 'pushButton'
    toggleSwitch = 'toggleSwitch'
    switch = 'switch'
    standbyPowerSwitch = 'standbyPowerSwitch'
    statelessPowerToggle = 'statelessPowerToggle'
    playPause = 'playPause'
    playStop = 'playStop'


class DisplayType1(Enum):
    stepper = 'stepper'
    feature = 'feature'


class DisplayType2(Enum):
    toggleSwitch = 'toggleSwitch'
    standbyPowerSwitch = 'standbyPowerSwitch'
    switch = 'switch'
    slider = 'slider'
    pushButton = 'pushButton'
    textButton = 'textButton'
    playPause = 'playPause'
    playStop = 'playStop'
    list = 'list'
    textField = 'textField'
    numberField = 'numberField'
    stepper = 'stepper'
    state = 'state'


class DisplayType3(Enum):
    toggleSwitch = 'toggleSwitch'
    standbyPowerSwitch = 'standbyPowerSwitch'
    switch = 'switch'
    slider = 'slider'
    pushButton = 'pushButton'
    textButton = 'textButton'
    playPause = 'playPause'
    playStop = 'playStop'
    list = 'list'
    textField = 'textField'
    numberField = 'numberField'
    stepper = 'stepper'
    state = 'state'
    multiArgCommand = 'multiArgCommand'


class DisplayType4(Enum):
    slider = 'slider'
    list = 'list'
    numberField = 'numberField'
    textField = 'textField'
    enumSlider = 'enumSlider'


class DisplayType5(Enum):
    slider = 'slider'
    list = 'list'
    numberField = 'numberField'
    textField = 'textField'
    multiArgCommand = 'multiArgCommand'


class DisplayType6(Enum):
    slider = 'slider'
    list = 'list'
    numberField = 'numberField'
    textField = 'textField'
    enumSlider = 'enumSlider'


class DisplayType7(Enum):
    slider = 'slider'
    list = 'list'
    textField = 'textField'
    numberField = 'numberField'
    multiArgCommand = 'multiArgCommand'


class Group(BaseModel):
    __root__: str = Field(
        ...,
        description='The group name to which this belongs. Some complex devices can be shown grouped in the dashboard card. This is used for grouping states and actions in the dashboard.',
        example='main',
    )


class FeatureItem(BaseModel):
    key: str = Field(
        ...,
        description='The name of the feature to be added to the detail view. For example, if the feature is specified as "cooking", then a detail view item will be added called "cooking"',
    )
    value: str = Field(..., description="The alternative string of given 'key' value.")


class Feature(BaseModel):
    __root__: List[FeatureItem] = Field(
        ...,
        description='Including a basicPlus item with the “feature” display type adds a shortcut item to the desired detail view.',
        example=[
            {'key': 'cooking', 'value': 'Cooking mode'},
            {'key': 'cleaning', 'value': 'Cleaning mode'},
        ],
    )


class Operator1(Enum):
    EQUALS = 'EQUALS'
    GREATER_THAN_OR_EQUALS = 'GREATER_THAN_OR_EQUALS'
    LESS_THAN_OR_EQUALS = 'LESS_THAN_OR_EQUALS'


class SupportedOperator(BaseModel):
    operator: Operator1 = Field(
        ..., description='The operator to be supported by this display type.'
    )
    label: str = Field(..., description='The alternative string of given operator.')


class DisplayType8(Enum):
    slider = 'slider'
    list = 'list'
    textField = 'textField'
    numberField = 'numberField'


class ArgumentName(BaseModel):
    __root__: str = Field(..., description='Argument name of a command')


class Button(BaseModel):
    key: str = Field(
        ...,
        description='A command name or an argument name of a command to be mapped with this button.',
        example='cooling',
    )
    label: str = Field(
        ...,
        description='The alternative string to be displayed when the `key` is evaluated.',
        example='Cooling',
    )
    state: Optional[str] = Field(
        None,
        description='To focus this button according to the current status of given attribute which is mapped with this button.',
        example='Cooling',
    )


class ValueModel(BaseModel):
    class Config:
        extra = Extra.allow

    __root__: constr(regex=r'(^[[a-z]*([A-Z][a-z]*)*){1,36}(\.value)+') = Field(
        ...,
        description='Notation which indicates the value of an attribute',
        example='switch.value',
    )


class UnitModel(BaseModel):
    __root__: constr(regex=r'(^[[a-z]*([A-Z][a-z]*)*){1,36}(\.unit)+') = Field(
        ..., example='temperature.unit'
    )


class ExcludeItemsCommand(BaseModel):
    name: str
    excludedValues: Optional[List[str]] = Field(
        None, description='To exclude only some values of the attribute'
    )


class ExcludeItemsCommands(BaseModel):
    __root__: List[ExcludeItemsCommand]


class ExcludeItemsAttribute(BaseModel):
    name: str = Field(..., description='Attribute name to be excluded')
    excludedValues: Optional[List[str]] = Field(
        None, description='To exclude only some values of the attribute'
    )


class ExcludeItemsAttributes(BaseModel):
    __root__: List[ExcludeItemsAttribute]


class ValueTypeModel(BaseModel):
    __root__: str = Field(
        ...,
        description="The data type of the `value`. It's automatically filled from the given capability.",
        example='double',
    )


class ArgumentType(BaseModel):
    __root__: str = Field(
        ...,
        description="The data type of the `argument`. It's automatically filled from the given capability.",
        example='double',
    )


class Op(Enum):
    add = 'add'
    replace = 'replace'
    remove = 'remove'


class PatchItem(BaseModel):
    op: Op = Field(
        ...,
        description='Operation objects MUST have exactly one "op" member, whose value indicates the operation to perform',
        example='replace',
    )
    path: str = Field(
        ...,
        description='path specifies a string format for identifying a specific value within a JSON document. It is used by all operations in patch to specify the part of the document to operate on.',
        example='/0/alternatives/1/value',
    )
    value: Optional[Dict[str, Any]] = Field(None, example='Focus mode')


class Idx(BaseModel):
    __root__: int = Field(
        ...,
        description='An index among the multiple items of dashboard provided in the capability presentation.',
    )


class Composite(BaseModel):
    __root__: bool = Field(
        ...,
        description='To specify composite use of different state items. If composite is true, multiple states items in the same group are combined to a label.',
    )


class Type6(Enum):
    remainingTime = 'remainingTime'
    time = 'time'


class TimeFormat(BaseModel):
    __root__: constr(regex=r'hh:mm(:ss){0,1}') = Field(..., example='hh:mm:ss')


class DeviceEventSource(Enum):
    OCFDEVICE = 'OCFDEVICE'
    HUBDEVICE = 'HUBDEVICE'
    HUB = 'HUB'
    CLOUD = 'CLOUD'


class DriverVersion(BaseModel):
    __root__: str = Field(
        ..., description='The version of the driver revision being returned'
    )


class PermissionAttributes(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class DeviceIntegrationProfileKey(BaseModel):
    id: Optional[UUID] = Field(
        None, description='Unique identifier for integration profile.'
    )
    majorVersion: Optional[int] = Field(
        None, description='Major Version of the integration profile'
    )


class PackageKey(BaseModel):
    __root__: constr(regex=r'^[a-zA-Z0-9 _/\\\-()\\[\\]{}\.]{1,36}$') = Field(
        ...,
        description="A user scoped package key that's used to lookup the respective driver record",
        example='smartthings.zigbee.bulb-rgbw',
    )


class DriverName(BaseModel):
    __root__: str = Field(
        ..., description='The name of the driver', example='Generic Button'
    )


class FingerprintId(BaseModel):
    __root__: str = Field(
        ...,
        description='The identifier for the respective fingerprint, unique per driver',
        example='smartthings.motion-v4',
    )


class FingerprintType(Enum):
    DTH = 'DTH'
    ZIGBEE_GENERIC = 'ZIGBEE_GENERIC'
    ZIGBEE_MANUFACTURER = 'ZIGBEE_MANUFACTURER'
    ZWAVE_MANUFACTURER = 'ZWAVE_MANUFACTURER'
    ZWAVE_GENERIC = 'ZWAVE_GENERIC'


class FingerprintDeviceLabel(BaseModel):
    __root__: str = Field(
        ...,
        description='Label assigned to device at join time. If this is not set the driver name is used.',
        example='Motion Sensor',
    )


class ZigbeeProfiles(BaseModel):
    __root__: List[int] = Field(
        ...,
        description='Device profiles associated with a generic zigbee fingerprint',
        example=[260],
    )


class ZigbeeManufacturer(BaseModel):
    __root__: constr(min_length=0, max_length=32) = Field(
        ..., description='Reported manufacturer of the device', example='SmartThings'
    )


class ZigbeeModel(BaseModel):
    __root__: constr(min_length=0, max_length=32) = Field(
        ..., description='Reported model of the device', example='motionv4'
    )


class ZigbeeManufacturerFingerprint(BaseModel):
    manufacturer: Optional[ZigbeeManufacturer] = None
    model: Optional[ZigbeeModel] = None
    deviceIntegrationProfileKey: Optional[DeviceIntegrationProfileKey] = None


class ZWaveManufacturerId(BaseModel):
    __root__: conint(ge=0, le=65535) = Field(
        ...,
        description='16-bit manufacturer identifier assigned by the Z-Wave Specification',
        example=134,
    )


class ZWaveProductId(BaseModel):
    __root__: conint(ge=0, le=65535) = Field(
        ..., description='16-bit manufacturer defined product identifier', example=12336
    )


class ZWaveProductType(BaseModel):
    __root__: conint(ge=0, le=65535) = Field(
        ..., description='16-bit manufacturer defined product type', example=17488
    )


class ZWaveGenericType(BaseModel):
    __root__: conint(ge=0, le=255) = Field(
        ..., description='8-bit indicator for the generic type of the device', example=6
    )


class ZWaveSpecificType(BaseModel):
    __root__: conint(ge=0, le=255) = Field(
        ...,
        description='8-bit indicator for the specific type of the device',
        example=6,
    )


class CommandClasses(BaseModel):
    either: Optional[List[conint(ge=0, le=255)]] = Field(
        None,
        description='List of 8-bit command class identifiers to match regardless of controlled or supported',
    )
    controlled: Optional[List[conint(ge=0, le=255)]] = Field(
        None, description='List of 8-bit command class identifiers that are controlled'
    )
    supported: Optional[List[conint(ge=0, le=255)]] = Field(
        None, description='List of 8-bit command class identifiers that are supported'
    )


class ClientClusters(BaseModel):
    __root__: List[conint(ge=0, le=65535)] = Field(
        ..., description='List of 16-bit cluster identifiers for client clusters'
    )


class ServerClusters(BaseModel):
    __root__: List[conint(ge=0, le=65535)] = Field(
        ..., description='List of 16-bit cluster identifiers for server clusters'
    )


class DeviceIdentifiers(BaseModel):
    __root__: List[int] = Field(
        ...,
        description='Device Identifiers associated with a generic zigbee fingerprint',
        example=[257],
    )


class ChannelType(Enum):
    DRIVER = 'DRIVER'


class ChannelId(BaseModel):
    __root__: UUID = Field(
        ...,
        description='The identifier of the Sprocket channel',
        example='9314a926-528c-403f-ae56-4b0d059381dd',
    )


class DetailedChannel(BaseModel):
    channelId: Optional[ChannelId] = None
    name: Optional[str] = Field(None, description='Name of the channel')
    description: Optional[str] = Field(None, description='Description of the channel')
    type: Optional[ChannelType] = None
    termsOfServiceUrl: Optional[str] = Field(
        None,
        description='URL for a developer-provided Terms of Service agreement for the channel',
    )
    createdDate: Optional[str] = Field(
        None,
        description='The ISO-8601 formatted timestamp when the channel was created',
    )
    lastModifiedDate: Optional[str] = Field(
        None,
        description='The ISO-8601 formatted timestamp when the channel was last modified',
    )


class PagedDetailedChannels(BaseModel):
    items: List[DetailedChannel]
    _links: Optional[Links] = None


class PatchChannel(BaseModel):
    name: Optional[str] = Field(None, description='Name of the channel')
    description: Optional[str] = Field(None, description='Description of the channel')
    termsOfServiceUrl: Optional[str] = Field(
        None,
        description='URL for a developer-provided Terms of Service agreement for the channel',
    )


class DriverRevision(BaseModel):
    driverId: Optional[DriverId] = None
    version: Optional[DriverVersion] = None


class DriverChannel(BaseModel):
    channelId: Optional[ChannelId] = None
    driverId: Optional[DriverId] = None
    version: Optional[DriverVersion] = None
    createdDate: Optional[str] = Field(
        None,
        description='The ISO-8601 formatted timestamp when the channel was created',
    )
    lastModifiedDate: Optional[str] = Field(
        None,
        description='The ISO-8601 formatted timestamp when the channel was last modified',
    )


class PagedDriverChannels(BaseModel):
    items: List[DriverChannel]
    _links: Optional[Links] = None


class UpdateDriverChannel(BaseModel):
    version: Optional[DriverVersion] = None


class PrincipalType1(Enum):
    RAW = 'RAW'


class OrganizationMember(BaseModel):
    principal: Optional[UUID] = Field(
        None,
        description='A raw user principal (user uuid).',
        example='7b8514e6-230d-41cc-b3c2-512bca15abf0',
    )
    principalType: Optional[PrincipalType1] = Field('RAW', example='RAW')


class Email(BaseModel):
    __root__: str = Field(
        ...,
        description='The E-mail address of the invited party.',
        example='person@people.net',
    )


class Role(Enum):
    ADMIN = 'ADMIN'
    DEVELOPER = 'DEVELOPER'


class Modification(Enum):
    REMOVE = 'REMOVE'
    CHANGE_ROLE = 'CHANGE_ROLE'


class Label(BaseModel):
    __root__: str = Field(
        ...,
        description='A pretty name for a developer organization.',
        example="Shoes n' Boots",
    )


class ManufacturerName(BaseModel):
    __root__: str = Field(
        ..., description='Manufacturer name for the organization.', example='ShoeBoots'
    )


class MnId(BaseModel):
    __root__: str = Field(
        ...,
        description='Legacy `mnId` (also `mnid`) field used by some Samsung services.',
        example='ShoeBoots',
    )


class OrganizationName(BaseModel):
    __root__: str = Field(
        ...,
        description='A unique name for an organization. Alphanumeric names only (no spaces or special characters)\nmust start with a letter. This will be the "namespace" for the custom capabilities for this org.',
        example='shoesNBoots1',
    )


class WarehouseGroupId(BaseModel):
    __root__: UUID = Field(
        ...,
        description='The groupId that corresponds to this organization in warehouse.',
        example='81bfb21a-8716-410b-b2c7-40c14f585b60',
    )


class ErrorResponse(BaseModel):
    requestId: Optional[str] = Field(
        None,
        description='A correlation id used for reference when contacting support.',
        example='7b8514e6-230d-41cc-b3c2-512bca15abf0',
    )
    error: Optional[Error] = None


class DeviceComponent(BaseModel):
    id: str = Field(..., example='main')
    label: Optional[str] = Field(None, description='UTF-8 label for the component.')
    capabilities: List[CapabilityReference]
    categories: List[DeviceCategory] = Field(
        ...,
        description='Defines the categories for the device. There can be up to 2, one defined by the manufacturer the other is a user selected value.\n',
        max_items=2,
    )
    restrictions: Optional[Restriction] = None
    icon: Optional[str] = Field(None, description='A user selected icon value\n')


class DeviceCommandsRequest(BaseModel):
    commands: Optional[List[DeviceCommand]] = Field(
        None, description='An array of commands to execute on the Device.'
    )


class DeviceStatus(BaseModel):
    components: Optional[Dict[str, ComponentStatus]] = Field(
        None,
        description='A map of componentId to Component status.',
        example={
            'main': {
                'switch': {'switch': {'value': 'on'}},
                'switchLevel': {'level': {'value': 90}},
            }
        },
    )
    healthState: Optional[HealthState] = None


class DeviceEventsRequest(BaseModel):
    deviceEvents: Optional[List[DeviceStateEvent]] = Field(
        None,
        description='An array of attribute state updates.',
        max_items=8,
        min_items=1,
    )


class AppDeviceDetails(BaseModel):
    installedAppId: Optional[str] = Field(
        None,
        description='The ID of the installed app that integrates this device.',
        example='0c0b935d-0616-4441-a0bf-da7aeec3dc0a',
    )
    externalId: Optional[constr(max_length=64)] = Field(
        None,
        description='A field to store an ID from a system external to SmartThings.',
        example='Th13390',
    )
    profile: Optional[DeviceProfileReference] = None


class DthDeviceDetails(BaseModel):
    completedSetup: bool = Field(
        ...,
        description='True if the device setup has been completed so the device is ready to use.',
    )
    deviceNetworkType: Optional[DeviceNetworkType] = None
    deviceTypeId: str = Field(
        ...,
        description="The identifier for the device's DeviceType.",
        example='7b8514e6-230d-41cc-b3c2-512bca15abf0',
    )
    deviceTypeName: str = Field(
        ...,
        description="The name for the device's DeviceType.",
        example='x.com.samsung.da.fridge',
    )
    executingLocally: Optional[ExecutingLocally] = None
    hubId: Optional[HubId] = None
    installedGroovyAppId: Optional[str] = Field(
        None,
        description='The ID of the installed groovy application',
        example='8f5ra619-4c05-4a90-a245-cc129b0a8098',
    )
    networkSecurityLevel: Optional[DeviceNetworkSecurityLevel] = None


class CommandResult(BaseModel):
    id: Optional[UUID] = Field(
        None, description='A UUID used for tracking the individual command.'
    )
    status: Optional[CommandStatus] = None


class LanDeviceDetails(BaseModel):
    networkId: Optional[DeviceNetworkId] = None
    driverId: Optional[DriverId] = None
    executingLocally: Optional[ExecutingLocally] = None
    hubId: Optional[HubId] = None
    provisioningState: Optional[ProvisioningState] = None


class ZigbeeDeviceDetails(BaseModel):
    eui: Optional[DeviceEui] = None
    networkId: Optional[DeviceNetworkId] = None
    driverId: Optional[DriverId] = None
    executingLocally: Optional[ExecutingLocally] = None
    hubId: Optional[HubId] = None
    provisioningState: Optional[ProvisioningState] = None


class ZwaveDeviceDetails(BaseModel):
    networkId: Optional[DeviceNetworkId] = None
    driverId: Optional[DriverId] = None
    executingLocally: Optional[ExecutingLocally] = None
    hubId: Optional[HubId] = None
    networkSecurityLevel: Optional[DeviceNetworkSecurityLevel] = None
    provisioningState: Optional[ProvisioningState] = None


class MatterDeviceDetails(BaseModel):
    driverId: Optional[DriverId] = None
    hubId: Optional[HubId] = None
    provisioningState: Optional[ProvisioningState] = None


class DeviceComponentReference(BaseModel):
    id: str = Field(..., example='main')
    label: Optional[str] = Field(
        None,
        description='A default label that will be used for a component. If this is not provided, it defaults to the componentId.\nIf there are translations for this component, the label defined there will take preference over this default label.',
        example='main',
    )
    capabilities: List[BaseCapabilityReference] = Field(
        ...,
        description='A list of `[ 1..20 ]` capabilities for this component.',
        max_items=20,
        min_items=1,
    )
    categories: Optional[List[DeviceCategory]] = None


class LocaleReference(BaseModel):
    tag: Optional[LocaleTag] = None


class PreferenceRequest(BaseModel):
    preferenceId: Optional[str] = Field(None, description='The ID of the preference')
    name: constr(regex=r'^[a-zA-Z0-9][a-zA-Z0-9 ]{1,35}$') = Field(
        ...,
        description='An alphanumeric English language name for this preference. Will be appended to a namespace to generate the full preference id.',
        example='tempOffset',
    )
    title: str = Field(
        ...,
        description='A short description for this preference.',
        example='Temperature Offset',
    )
    description: Optional[str] = Field(
        None,
        description='A long description for this preference.',
        example='The offset for a particular temperature setting',
    )
    explicit: Optional[bool] = Field(
        False,
        description='A flag describing whether this preference is explicit, or inline.',
    )
    required: Optional[bool] = Field(
        False, description='A flag describing whether this property is required or not.'
    )
    preferenceType: PreferenceType
    definition: Definition = Field(
        ..., description='The definition of this preference.'
    )


class PreferenceResponse(BaseModel):
    preferenceId: Optional[str] = Field(None, description='The ID of the preference')
    name: Optional[str] = Field(
        None, description='An alphanumeric English language name for this preference.'
    )
    title: str = Field(
        ...,
        description='A short description for this preference.',
        example='Temperature Offset',
    )
    description: Optional[str] = Field(
        None,
        description='A long description for this preference.',
        example='The offset for a particular temperature setting',
    )
    required: Optional[bool] = Field(
        False, description='A flag describing whether this property is required or not.'
    )
    preferenceType: PreferenceType


class PagedPreferences(BaseModel):
    items: Optional[List[PreferenceResponse]] = None
    _links: Optional[Links] = None


class SmartAppDashboardCardEventRequest(BaseModel):
    cardId: Optional[str] = Field(
        None,
        description='A developer defined dashboard card ID.',
        example='my_dashboard_card',
    )
    lifecycle: Optional[DashboardCardLifecycle] = None


class LocationParent(BaseModel):
    type: Optional[LocationParentTypes] = None
    id: Optional[constr(min_length=36, max_length=36)] = Field(
        None, description='The ID of the parent'
    )


class PagedRooms(BaseModel):
    items: Optional[List[Room]] = None
    _links: Optional[Links] = None


class Delivery(BaseModel):
    deliveryType: Optional[DeliveryType] = None
    deliveryTarget: Optional[str] = Field(
        None, description='Target for the delivery type.'
    )


class InstallConfiguration(BaseModel):
    installedAppId: Optional[UUID] = Field(
        None, description='The ID of the installed app.'
    )
    configurationId: Optional[UUID] = Field(
        None, description='The ID to this configration instance.'
    )
    configurationStatus: Optional[InstallConfigurationStatus] = None
    createdDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )
    lastUpdatedDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )


class InstallConfigurationDetail(BaseModel):
    installedAppId: Optional[UUID] = Field(
        None, description='The ID of the installed app.'
    )
    configurationId: Optional[UUID] = Field(
        None, description='The ID to this configration instance.'
    )
    configurationStatus: Optional[InstallConfigurationStatus] = None
    config: Optional[ConfigMap] = None
    createdDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )
    lastUpdatedDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )


class PagedInstallConfigurations(BaseModel):
    items: Optional[List[InstallConfiguration]] = None
    _links: Optional[Links] = None


class CreateInstalledAppEventsRequest(BaseModel):
    smartAppEvents: Optional[List[SmartAppEventRequest]] = Field(
        None,
        description='An array of smartapp events used to trigger client behavior in loaded web plugin detail pages.  Events will\nbe delivered to JavaScript event handler of all active client processes related to parameterized installed app.\n',
        max_items=8,
        min_items=1,
    )
    smartAppDashboardCardEvents: Optional[
        List[SmartAppDashboardCardEventRequest]
    ] = Field(
        None,
        description='An array of smartapp dashboard card events used to trigger client behavior for dashboard cards.\nDashboard card events are directives to a SmartThings client to take actions in relation to lifecycle changes\nto a specific dashboard card.  These events are not delivered to the web plugin event handler.\n',
        max_items=8,
        min_items=1,
    )


class Notice(BaseModel):
    code: Optional[NoticeCode] = None
    badgeUrl: Optional[str] = Field(
        None, description='The url of the badge icon for the notice card'
    )
    message: Optional[str] = Field(
        None, description='The localized message to be displayed'
    )
    actions: Optional[List[NoticeAction]] = Field(
        None, description='The action(s) a user can take to resolve this notice'
    )


class Subscription(BaseModel):
    id: Optional[str] = Field(
        None,
        description='The id of the subscription.',
        example='736e3903-001c-4d40-b408-ff40d162a06b',
    )
    installedAppId: Optional[str] = Field(
        None,
        description='The id of the subscribing app.',
        example='499e28ba-b33b-49c9-a5a1-cce40e41f8a6',
    )
    sourceType: Optional[SubscriptionSource] = None
    device: Optional[DeviceSubscriptionDetail] = None
    capability: Optional[CapabilitySubscriptionDetail] = None
    mode: Optional[ModeSubscriptionDetail] = None
    deviceLifecycle: Optional[DeviceLifecycleDetail] = None
    deviceHealth: Optional[DeviceHealthDetail] = None
    securityArmState: Optional[SecurityArmStateDetail] = None
    hubHealth: Optional[HubHealthDetail] = None
    sceneLifecycle: Optional[SceneLifecycleDetail] = None


class SubscriptionRequest(BaseModel):
    sourceType: str
    device: Optional[DeviceSubscriptionDetail] = None
    capability: Optional[CapabilitySubscriptionDetail] = None
    mode: Optional[ModeSubscriptionDetail] = None
    deviceLifecycle: Optional[DeviceLifecycleDetail] = None
    deviceHealth: Optional[DeviceHealthDetail] = None
    securityArmState: Optional[SecurityArmStateDetail] = None
    hubHealth: Optional[HubHealthDetail] = None
    sceneLifecycle: Optional[SceneLifecycleDetail] = None


class PagedSubscriptions(BaseModel):
    items: Optional[List[Subscription]] = None
    _links: Optional[Links] = None


class SubscriptionFilter(BaseModel):
    type: Optional[SubscriptionFilterTypes] = None
    value: Optional[SubscriptionFilterValues] = None
    eventType: Optional[SubscriptionFilterEventTypes] = None
    attribute: Optional[SubscriptionFilterAttributes] = None
    capability: Optional[SubscriptionFilterCapabilities] = None
    component: Optional[SubscriptionFilterComponents] = None


class SubscriptionTarget(BaseModel):
    url: Optional[SubscriptionTargetValue] = None


class PagedApp(BaseModel):
    appName: Optional[str] = Field(
        None,
        description='A user defined unique identifier for an app.  It is alpha-numeric, may contain dashes,\nunderscores, periods, and be less then 250 characters long.  It must be unique within your account.\n',
    )
    appId: Optional[UUID] = Field(
        None, description='A globally unique identifier for an app.'
    )
    appType: Optional[AppType] = None
    classifications: Optional[List[str]] = Field(
        None,
        description='An App maybe associated to many classifications.  A classification drives how the integration is presented\nto the user in the SmartThings mobile clients.  These classifications include:\n* AUTOMATION - Denotes an integration that should display under the "Automation" tab in mobile clients.\n* SERVICE - Denotes an integration that is classified as a "Service".\n* DEVICE - Denotes an integration that should display under the "Device" tab in mobile clients.\n* CONNECTED_SERVICE - Denotes an integration that should display under the "Connected Services" menu in mobile clients.\n* HIDDEN - Denotes an integration that should not display in mobile clients\n',
    )
    displayName: Optional[constr(max_length=75)] = Field(
        None, description='A default display name for an app.\n'
    )
    description: Optional[constr(max_length=250)] = Field(
        None, description='A default description for an app.\n'
    )
    iconImage: Optional[IconImageModel] = None
    owner: Optional[Owner] = None
    createdDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )
    lastUpdatedDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )


class WebhookSmartApp(BaseModel):
    targetUrl: Optional[str] = Field(
        None, description='A URL that should be invoked during execution.'
    )
    targetStatus: Optional[AppTargetStatus] = None
    publicKey: Optional[str] = Field(
        None,
        description='The public half of an RSA key pair.  Useful for verifying a Webhook execution request signature to\nensure it came from SmartThings.\n',
    )
    signatureType: Optional[SignatureType] = None


class CreateAppRequest(BaseModel):
    appName: str = Field(
        ...,
        description='A globally unique, developer-defined identifier for an app. It is alpha-numeric, may contain dashes,\nunderscores, periods, and must be less then 250 characters long.\n',
    )
    displayName: constr(max_length=75) = Field(
        ..., description='A default display name for an app.\n'
    )
    description: constr(max_length=250) = Field(
        ..., description='A default description for an app.\n'
    )
    singleInstance: Optional[bool] = Field(
        False,
        description="Inform the installation systems that a particular app can only be installed once within a user's account.\n",
    )
    iconImage: Optional[IconImageModel] = None
    appType: str
    principalType: Optional[PrincipalTypeModel] = None
    classifications: List[str] = Field(
        ...,
        description='An App maybe associated to many classifications.  A classification drives how the integration is presented\nto the user in the SmartThings mobile clients.  These classifications include:\n* AUTOMATION - Denotes an integration that should display under the "Automation" tab in mobile clients.\n* SERVICE - Denotes an integration that is classified as a "Service".\n* DEVICE - Denotes an integration that should display under the "Device" tab in mobile clients.\n* CONNECTED_SERVICE - Denotes an integration that should display under the "Connected Services" menu in mobile clients.\n* HIDDEN - Denotes an integration that should not display in mobile clients\n',
    )
    lambdaSmartApp: Optional[CreateOrUpdateLambdaSmartAppRequest] = None
    webhookSmartApp: Optional[CreateOrUpdateWebhookSmartAppRequest] = None
    oauth: Optional[AppOAuth] = None
    ui: Optional[AppUISettings] = None


class UpdateAppRequest(BaseModel):
    displayName: constr(max_length=75) = Field(
        ..., description='A default display name for an app.\n'
    )
    description: constr(max_length=250) = Field(
        ..., description='A default description for an app.\n'
    )
    singleInstance: Optional[bool] = Field(
        False,
        description="Inform the installation systems that a particular app can only be installed once within a user's account.\n",
    )
    iconImage: Optional[IconImageModel] = None
    appType: AppType
    classifications: List[AppClassification] = Field(
        ...,
        description='An App maybe associated to many classifications.  A classification drives how the integration is presented\nto the user in the SmartThings mobile clients.  These classifications include:\n* AUTOMATION - Denotes an integration that should display under the "Automation" tab in mobile clients.\n* SERVICE - Denotes an integration that is classified as a "Service".\n* DEVICE - Denotes an integration that should display under the "Device" tab in mobile clients.\n* CONNECTED_SERVICE - Denotes an integration that should display under the "Connected Services" menu in mobile clients.\n* HIDDEN - Denotes an integration that should not display in mobile clients\n',
    )
    lambdaSmartApp: Optional[CreateOrUpdateLambdaSmartAppRequest] = None
    webhookSmartApp: Optional[CreateOrUpdateWebhookSmartAppRequest] = None
    ui: Optional[AppUISettings] = None


class UpdateSignatureTypeRequest(BaseModel):
    signatureType: Optional[SignatureType] = None


class AdhocMessage(BaseModel):
    fallbackLocale: LocaleTag
    defaultVariables: Optional[Dict[str, str]] = Field(
        None,
        description='A map<string,string> with the key representing the variable name, and the value representing the verbiage\nto be replaced in template string. `defaultVariables` will only be used if there are no matching locale-level\n(template) variables for that key.\n',
    )
    templates: List[AdhocMessageTemplate] = Field(
        ...,
        description='A list of templates representing the same message in different languages.',
        max_items=35,
        min_items=1,
    )


class Message(BaseModel):
    fallbackLocale: LocaleTag
    templates: List[MessageTemplate] = Field(
        ...,
        description='A list of templates representing the same message in different languages.',
        max_items=35,
        min_items=1,
    )


class CommandAction(BaseModel):
    devices: List[str]
    commands: List[DeviceCommand]
    sequence: Optional[CommandSequence] = Field(
        None,
        description='The sequence in which the commands are to be executed i.e. Serial or Parallel (default)',
    )


class DateOperand(BaseModel):
    timeZoneId: Optional[str] = Field(None, description='A java time zone ID reference')
    daysOfWeek: Optional[List[DayOfWeek]] = None
    year: Optional[int] = None
    month: Optional[conint(ge=1, le=12)] = None
    day: Optional[conint(ge=1, le=31)] = None
    reference: Optional[DateReference] = None


class DeviceOperand(BaseModel):
    devices: List[str]
    component: str
    capability: str
    attribute: str
    path: Optional[str] = None
    aggregation: Optional[OperandAggregationMode] = None
    trigger: Optional[TriggerMode] = None


class LocationOperand(BaseModel):
    locationId: Optional[str] = Field(
        None,
        description='Required for User level rule, optional for Location level in request. Will always be present in response for both.',
    )
    attribute: LocationAttribute
    trigger: Optional[TriggerMode] = None


class SceneCommand(BaseModel):
    arguments: Optional[List[SceneArgument]] = Field(
        None, description='the command arguments'
    )


class PagedCapabilities(BaseModel):
    items: Optional[List[CapabilitySummary]] = None
    _links: Optional[Links] = None


class AttributeSchema(BaseModel):
    class Config:
        extra = Extra.forbid

    title: Optional[str] = Field(None, description="The capability's name, no spaces.")
    type: Optional[Type] = Field(
        None,
        description='For schema this will always be object and is the only allowed value.',
    )
    properties: AttributeProperties
    additionalProperties: Optional[AdditionalProperties] = None
    required: Optional[List[RequiredEnum]] = Field(
        None, description='Provide requirement for `value`, `unit`, and `data` fields.'
    )


class CapabilityCommand(BaseModel):
    name: constr(regex=r'^[[a-z]*([A-Z][a-z]*)*]{1,36}$') = Field(
        ...,
        description='The name of the command. Unique for the capability',
        example='setTemperature',
    )
    arguments: Optional[List[Argument]] = Field(
        None,
        description='An array of argument definitions. The arguments must be supplied in the order specified.',
    )


class CapabilityLocaleLocalizations(BaseModel):
    items: Optional[List[LocaleReference]] = None


class Subscription1(BaseModel):
    subscriptionId: str = Field(..., description='subscription ID')
    geoplaceId: Optional[str] = Field(
        None,
        description='Geo Place ID (This ID is only supported in "alert" capability)\n',
    )
    type: str = Field(
        ..., description='DIRECT or EXECUTION delivery, default to DIRECT'
    )
    predicate: Optional[str] = Field(None, description='JEXL expression string')
    subscribedCapabilities: ServiceCapabilities


class ServiceLocationInfo(BaseModel):
    locationId: str = Field(..., description='location ID')
    subscriptions: List[Subscription1]
    latitude: float = Field(..., description='latitude')
    longitude: float = Field(..., description='longitude')
    city: str = Field(..., description='city')


class Isa(BaseModel):
    pageType: Optional[str] = Field(
        None,
        description='Possible values - __requiresLogin__ or __loggedIn__. These two values determine what fields are returned in this response. If value is "requiresLogin", only "oAuthLink" is returned in the response. If value is "loggedIn", only isaId, partnerName, appName, devices and icons are returned.',
    )
    isaId: Optional[str] = Field(None, description='isaId (Installed App Id)')
    endpointAppId: Optional[str] = Field(
        None, description='endpoint app id of the installed smart app'
    )
    partnerName: Optional[str] = Field(
        None, description='partner or brand name eg LIFX Inc.'
    )
    appName: Optional[str] = Field(
        None, description='Connector name. eg Lifx (Connect)'
    )
    icon: Optional[str] = Field(None, description='url of partner icon')
    icon2x: Optional[str] = Field(
        None, description='url of partner icon in 2x dimensions'
    )
    icon3x: Optional[str] = Field(
        None, description='url of partner icon in 3x dimensions'
    )
    locationId: Optional[str] = Field(
        None, description='location of the installed smart app'
    )
    devices: Optional[List[DeviceResults]] = None
    oAuthLink: Optional[str] = Field(
        None,
        description='generated oAuth link for the user to login to partner server. This will only be returned when the user is not logged in.',
    )
    viperAppLinks: Optional[ViperAppLinks] = None
    partnerSTConnection: Optional[PartnerSTConnection] = Field(
        None, description='connection status between partner and ST platform'
    )


class LocationIsa(BaseModel):
    installedSmartApps: Optional[List[IsaResults]] = None


class PostEndpointApp(BaseModel):
    appName: Optional[str] = Field(
        None, description='The name of the SmartThings Schema App'
    )
    partnerName: str = Field(..., description='The name of the partner/brand')
    oAuthAuthorizationUrl: str = Field(
        ..., description='oAuth authorization url of the partner'
    )
    lambdaArn: Optional[str] = Field(
        None, description='lambda arn of the partner for US region (default)'
    )
    lambdaArnEU: Optional[str] = Field(
        None, description='lambda arn of the partner for EU region'
    )
    lambdaArnAP: Optional[str] = Field(
        None, description='lambda arn of the partner for AP region'
    )
    lambdaArnCN: Optional[str] = Field(
        None, description='lambda arn of the partner for CN region'
    )
    icon: Optional[str] = Field(None, description='url of partner icon')
    icon2x: Optional[str] = Field(
        None, description='url of partner icon in 2x dimensions'
    )
    icon3x: Optional[str] = Field(
        None, description='url of partner icon in 3x dimensions'
    )
    endpointAppId: Optional[str] = Field(
        None, description='SmartThings Schema App id for the partner'
    )
    oAuthClientId: str = Field(..., description='Client id for the partner oAuth')
    oAuthClientSecret: str = Field(
        ..., description='Client secret for the partner oAuth'
    )
    oAuthTokenUrl: str = Field(
        ..., description='oAuth token refresh url of the partner'
    )
    oAuthScope: Optional[str] = Field(
        None,
        description='oAuth scope for the partner. Example "remote_control:all" for Lifx',
    )
    userId: Optional[str] = Field(None, description='user id for the partner')
    hostingType: str = Field(..., description='Possible values - "lambda" or "webhook"')
    schemaType: Optional[str] = Field(
        None,
        description='Possible values - "alexa-schema", "st-schema", "google-schema"',
    )
    webhookUrl: Optional[str] = Field(None, description='webhook url for the partner')
    certificationStatus: Optional[str] = Field(
        None, description='Possible values - "", "cst", "wwst", "review"'
    )
    userEmail: Optional[str] = Field(None, description='Email for the partner')
    viperAppLinks: Optional[ViperAppLinks] = None


class EndpointApp(BaseModel):
    appName: Optional[str] = Field(
        None, description='The name of the SmartThings Schema App'
    )
    partnerName: Optional[str] = Field(
        None, description='The name of the partner/brand'
    )
    oAuthAuthorizationUrl: Optional[str] = Field(
        None, description='oAuth authorization url of the partner'
    )
    lambdaArn: Optional[str] = Field(
        None, description='lambda arn of the partner for US region (default)'
    )
    lambdaArnEU: Optional[str] = Field(
        None, description='lambda arn of the partner for EU region'
    )
    lambdaArnAP: Optional[str] = Field(
        None, description='lambda arn of the partner for AP region'
    )
    lambdaArnCN: Optional[str] = Field(
        None, description='lambda arn of the partner for CN region'
    )
    icon: Optional[str] = Field(None, description='url of partner icon')
    icon2x: Optional[str] = Field(
        None, description='url of partner icon in 2x dimensions'
    )
    icon3x: Optional[str] = Field(
        None, description='url of partner icon in 3x dimensions'
    )
    endpointAppId: Optional[str] = Field(
        None, description='endpoint app id for the partner'
    )
    oAuthClientId: Optional[str] = Field(
        None, description='Client id for the partner oAuth'
    )
    oAuthClientSecret: Optional[str] = Field(
        None, description='Client secret for the partner oAuth'
    )
    oAuthTokenUrl: Optional[str] = Field(
        None, description='oAuth token refresh url of the partner'
    )
    oAuthScope: Optional[str] = Field(
        None,
        description='oAuth scope for the partner. Example "remote_control:all" for Lifx',
    )
    userId: Optional[str] = Field(None, description='user id for the partner')
    hostingType: Optional[str] = Field(
        None, description='Possible values - "lambda" or "webhook"'
    )
    schemaType: Optional[str] = Field(
        None,
        description='Possible values - "alexa-schema", "st-schema", "google-schema"',
    )
    webhookUrl: Optional[str] = Field(None, description='webhook url for the partner')
    certificationStatus: Optional[str] = Field(
        None, description='Possible values - "", "cst", "wwst", "review"'
    )
    userEmail: Optional[str] = Field(None, description='Email for the partner')
    viperAppLinks: Optional[ViperAppLinks] = None


class TimerEvent(BaseModel):
    eventId: Optional[str] = Field(None, description='The ID of the event.')
    name: Optional[str] = Field(
        None,
        description='The name of the schedule that caused this event.',
        example='lights_off_timeout',
    )
    type: Optional[TimerType] = None
    time: Optional[datetime] = Field(
        None,
        description='The IS0-8601 date time strings in UTC that this event was scheduled for.',
        example='2017-08-04T12:44:18Z',
    )
    expression: Optional[str] = Field(
        None, description='The CRON expression if the schedule was of type CRON.'
    )


class DeviceCommandsEvent(BaseModel):
    eventId: Optional[str] = Field(None, description='The id of the event.')
    deviceId: Optional[str] = Field(
        None, description='The guid of the device that the commands are for.'
    )
    profileId: Optional[str] = Field(
        None, description='The device profile ID of the device instance.'
    )
    externalId: Optional[str] = Field(
        None, description='The external ID that was set during install of a device.'
    )
    commands: Optional[List[DeviceCommandsEventCommand]] = None


class DeviceLifecycleEvent(BaseModel):
    lifecycle: Optional[DeviceLifecycle] = None
    eventId: Optional[str] = Field(None, description='The id of the event.')
    locationId: Optional[str] = Field(
        None,
        description='The id of the location in which the event was triggered.\n\nThis field is not used or populated for user-level events.\n\nLocation id may also be sent in `ownerId` with `ownerType` = `LOCATION`.\n',
    )
    ownerId: Optional[str] = Field(
        None,
        description='ID for what owns the device lifecyle event. Works in tandem with `ownerType` as a composite identifier.',
    )
    ownerType: Optional[EventOwnerType] = None
    deviceId: Optional[str] = Field(None, description='The id of the device.')
    deviceName: Optional[str] = Field(None, description='The name of the device')
    principal: Optional[str] = Field(
        None, description='The principal that made the change'
    )
    create: Optional[DeviceLifecycleCreate] = None
    delete: Optional[DeviceLifecycleDelete] = None
    update: Optional[DeviceLifecycleUpdate] = None
    moveFrom: Optional[DeviceLifecycleMove] = None
    moveTo: Optional[DeviceLifecycleMove] = None
    roomMove: Optional[DeviceLifecycleRoomMove] = None


class SecurityArmStateEvent(BaseModel):
    eventId: Optional[str] = Field(None, description='The id of the event.')
    locationId: Optional[str] = Field(
        None, description='The id of the location in which the event was triggered.'
    )
    armState: Optional[ArmState1] = Field(
        None, description='The arm state of a security system.\n'
    )
    optionalArguments: Optional[Dict[str, SimpleValue]] = Field(
        None,
        description='A set of key / value pairs useful for passing any optional arguments.\n',
    )


class DeviceHealthEvent(BaseModel):
    eventId: Optional[str] = Field(None, description='The id of the event.')
    locationId: Optional[str] = Field(
        None,
        description='The id of the location in which the event was triggered.\n\nThis field is not used or populated for user-level events.\n\nLocation id may also be sent in `ownerId` with `ownerType` = `LOCATION`.\n',
    )
    ownerId: Optional[str] = Field(
        None,
        description='ID for what owns the device health event. Works in tandem with `ownerType` as a composite identifier.',
    )
    ownerType: Optional[EventOwnerType] = None
    deviceId: Optional[str] = Field(None, description='The id of the device.')
    hubId: Optional[str] = Field(None, description='The id of the hub.')
    status: Optional[Status5] = Field(None, description='The status of the device.\n')
    reason: Optional[Reason] = Field(
        None, description='The reason the device is offline.\n'
    )
    eventSource: Optional[DeviceEventSource] = None


class SceneLifecycleEvent(BaseModel):
    lifecycle: Optional[SceneLifecycle] = None
    eventId: Optional[str] = Field(None, description='The id of the event.')
    locationId: Optional[str] = Field(
        None, description='The id of the location in which the event was triggered.'
    )
    sceneId: Optional[str] = Field(None, description='The id of the scene.')
    version: Optional[str] = Field(None, description='The version of the scene.')
    migrateUuid: Optional[str] = Field(None, description='The migration owner uuid')
    create: Optional[SceneLifecycleCreate] = None
    update: Optional[SceneLifecycleUpdate] = None
    delete: Optional[SceneLifecycleDelete] = None
    createForBixby: Optional[SceneLifecycleCreateForBixby] = None
    updateForBixby: Optional[SceneLifecycleUpdateForBixby] = None
    deleteForBixby: Optional[SceneLifecycleDeleteForBixby] = None


class InstalledAppLifecycleEvent(BaseModel):
    eventId: Optional[str] = Field(None, description='The id of the event.')
    locationId: Optional[str] = Field(
        None,
        description='The ID of the location in which the event was triggered.',
        example='499e28ba-b33b-49c9-a5a1-cce40e41f8a6',
    )
    installedAppId: Optional[str] = Field(
        None,
        description='The ID of the installed application.',
        example='6f5ea629-4c05-4a90-a244-cc129b0a80c3',
    )
    appId: Optional[str] = Field(None, description='The ID of the application.')
    lifecycle: Optional[InstalledAppLifecycle] = None
    create: Optional[InstalledAppLifecycleCreate] = None
    install: Optional[InstalledAppLifecycleInstall] = None
    update: Optional[InstalledAppLifecycleUpdate] = None
    delete: Optional[InstalledAppLifecycleDelete] = None
    other: Optional[InstalledAppLifecycleOther] = None
    error: Optional[InstalledAppLifecycleError] = None


class GenerateConfigExclusion(ComponentId, BaseCapabilityReference, DeviceConfigView):
    pass


class LanguageItem(BaseModel):
    locale: str = Field(..., description='ICU locale')
    poCodes: List[PoCodes] = Field(
        ..., description='The list of resources that contain translated text'
    )


class AlternativeItem(BaseModel):
    key: str = Field(
        ...,
        description="The label string to be displayed when the 'key' is evaluated.",
        example='on',
    )
    value: str = Field(
        ...,
        description='The alternative string to be displayed when the `key` is selected.',
        example='Motion detected',
    )
    type: Optional[Type5] = Field(
        'active',
        description='This shows the active or inactive state of the value. Active is shown in color, while inactive value is shown dimmed in the UI view. For example, Motion sensor capability would have `detected` as active and in color and `clear` as inactive and dimmed so that a user can see the `detected` event easily.',
    )
    iconUrl: Optional[IconUrl] = None
    description: Optional[str] = Field(
        None,
        description='Additional description for each value. This description is shown in detail view or automation under this particular key.',
    )


class VisibleCondition(CapabilityKey):
    component: Optional[Component1] = Field(
        None,
        description='The component that controls the visibility of this component. This can be another component or this one.',
    )
    value: Optional[ValueModel] = None
    operator: Optional[Operator] = None
    operand: Optional[str] = Field(
        None, description='The value that the visible condition evaluates against.'
    )


class GroupVisibleConditions(CapabilityKey):
    component: Optional[Component1] = Field(
        None,
        description='The component that controls the visibility of this component. This can be another component or this one.',
    )
    value: Optional[ValueModel] = None
    operator: Optional[Operator] = None
    operand: Optional[str] = Field(
        None, description='The value that the visible condition evaluates against.'
    )


class NumberField(BaseModel):
    value: Optional[ValueModel] = None
    valueType: Optional[ValueTypeModel] = None
    unit: Optional[UnitModel] = None
    command: str
    argumentType: Optional[ArgumentType] = None
    range: Optional[Range] = None


class NumberFieldForAutomationAction(BaseModel):
    command: str
    argumentType: Optional[ArgumentType] = None
    unit: Optional[UnitModel] = None
    range: Optional[Range] = None


class NumberFieldForAutomationCondition(BaseModel):
    value: ValueModel
    valueType: Optional[ValueTypeModel] = None
    unit: Optional[UnitModel] = None
    range: Optional[Range] = None


class PushButton(BaseModel):
    command: str
    argument: Optional[str] = None
    argumentType: Optional[ArgumentType] = None


class SliderBase(BaseModel):
    range: Range
    step: Optional[Step] = None
    unit: Optional[UnitModel] = None


class SliderForAutomationAction(SliderBase):
    command: str
    argumentType: Optional[ArgumentType] = None


class SliderForAutomationCondition(SliderBase):
    value: ValueModel
    valueType: Optional[ValueTypeModel] = None


class Command1(BaseModel):
    name: Optional[str] = Field(
        None,
        description='To specify a single command like "setValue(number)", use “command” field for the command name. If this field is specified then "increase" and "descrease" fields should not be specified. App will calculate desired value when user clicks "+" and "-" button in the UI based on the current value of "attribute" with specified "step".',
    )
    increase: Optional[str] = Field(
        None, description='To specify a command for "increase" without an argument.'
    )
    decrease: Optional[str] = Field(
        None, description='To specify a command for "decrease" without an argument.'
    )
    argumentType: Optional[ArgumentType] = None


class Stepper(BaseModel):
    command: Command1
    value: Optional[ValueModel] = None
    valueType: Optional[ValueTypeModel] = None
    step: Step
    range: Range


class TextField(BaseModel):
    command: str
    argumentType: Optional[ArgumentType] = None
    value: Optional[ValueModel] = None
    valueType: Optional[ValueTypeModel] = None
    range: Optional[Range] = None


class TextFieldForAutomationAction(BaseModel):
    command: str
    argumentType: Optional[ArgumentType] = None
    range: Optional[Range] = None


class TextFieldForAutomationCondition(BaseModel):
    value: ValueModel
    valueType: Optional[ValueTypeModel] = None
    range: Optional[Range] = None


class SliderForArgument(SliderBase):
    name: ArgumentName
    argumentType: Optional[ArgumentType] = None


class TextFieldForArgument(BaseModel):
    name: ArgumentName
    argumentType: Optional[ArgumentType] = None
    range: Optional[Range] = None


class NumberFieldForArgument(BaseModel):
    name: ArgumentName
    argumentType: Optional[ArgumentType] = None
    range: Optional[Range] = None


class Command2(BaseModel):
    name: Optional[str] = None
    on: str
    off: str
    argumentType: Optional[ArgumentType] = None


class SwitchCommand(BaseModel):
    command: Command2 = Field(
        ...,
        description='To specify separate commands with no arguments for on and off, use the “on” and “off” fields respectively. To specify a single command, use “name” for the command and the “on” and “off” fields for the arguments.',
    )


class StatelessPowerToggleForDashboard(BaseModel):
    command: str
    argument: Optional[str] = None
    argumentType: Optional[ArgumentType] = None


class Command3(BaseModel):
    name: Optional[str] = None
    play: str
    pause: str
    argumentType: Optional[ArgumentType] = None


class PlayPauseCommand(BaseModel):
    command: Command3 = Field(
        ...,
        description='To specify separate commands with no arguments for on and off, use the “play” and “pause” fields respectively. To specify a single command, use “name” for the command and the “play” and “pause” fields for the arguments.',
    )


class Command4(BaseModel):
    name: Optional[str] = None
    play: str
    stop: str
    argumentType: Optional[ArgumentType] = None


class PlayStopCommand(BaseModel):
    command: Command4 = Field(
        ...,
        description='To specify separate commands with no arguments for on and off, use the “play” and “stop” fields respectively. To specify a single command, use “name” for the command and the “play” and “stop” fields for the arguments.',
    )


class TextButton(BaseModel):
    command: Optional[str] = Field(
        None,
        description='To specify command name with argument(s) and key of the buttons is the argument of the command. If this is omitted then keys at `buttons` array are the enumCommands without arguments.',
        example='setThermostatMode',
    )
    value: Optional[ValueModel] = None
    buttons: List[Button] = Field(..., min_items=2)
    supportedValues: Optional[SupportedValues] = None


class ExcludeItem(BaseModel):
    component: Optional[str] = Field(None, example='main')
    capability: str = Field(..., example='pictureMode')
    version: Optional[int] = Field(1, example=1)
    attributes: Optional[ExcludeItemsAttributes] = None


class ExcludedConditionItem(BaseModel):
    value: Optional[Dict[str, Any]] = Field(
        None, description='To express that a specific value is selected', example='HDMI'
    )
    exclude: List[ExcludeItem]


class ExcludeItem1(BaseModel):
    component: Optional[str] = Field(
        None,
        description="To specify target component to exclude, if it's omitted then all components with this capability will be excluded",
        example='main',
    )
    capability: str = Field(..., example='pictureMode')
    version: Optional[int] = Field(1, example=1)
    commands: Optional[ExcludeItemsCommands] = None


class ExcludedActionItem(BaseModel):
    value: Optional[Dict[str, Any]] = Field(
        None, description='To express that a specific value is selected', example='off'
    )
    exclude: List[ExcludeItem1]


class ExcludedConditionItemId(ExcludedConditionItem):
    id: Optional[int] = Field(
        None,
        description='The index of the array in the given capability to which this exclusion object will be inserted',
    )


class ExcludedActionItemId(ExcludedActionItem):
    id: Optional[int] = Field(
        None,
        description='The index of the array in the given capability to which this exclusion object will be inserted',
    )


class DeviceConfigEntryBase(BaseModel):
    component: str = Field(..., example='main')
    capability: str = Field(..., example='thermostatMode')
    version: Optional[Version] = None
    visibleCondition: Optional[VisibleCondition] = None


class DeviceConfigEntryForDashboardAction(DeviceConfigEntryBase):
    idx: Optional[Idx] = None
    group: Optional[Group] = None


class RemainingTime(BaseModel):
    timeFormat: TimeFormat
    frequency: Optional[int] = Field(
        60,
        description='Specify the frequency time(second) so UI client can know how often to update the remaing time.',
        example=60,
    )


class Time(BaseModel):
    timeFormat: TimeFormat


class FormatInfoItem(BaseModel):
    key: ValueModel
    type: Type6 = Field(
        ...,
        description='To specify the type of format to display this attribute value. The corresponding field must also be included. For example, if you specify "remainingTime" here, you must also include the "remainingTime" key and its object definition for formatInfo.',
        example='remainingTime',
    )
    remainingTime: Optional[RemainingTime] = None
    time: Optional[Time] = None


class FormatInfo(BaseModel):
    __root__: List[FormatInfoItem]


class DriverPermission(BaseModel):
    name: str = Field(..., description='Name of the permission')
    attributes: PermissionAttributes


class ZWaveManufacturerFingerprint(BaseModel):
    manufacturerId: Optional[ZWaveManufacturerId] = None
    productId: Optional[ZWaveProductId] = None
    productType: ZWaveProductType
    deviceIntegrationProfileKey: Optional[DeviceIntegrationProfileKey] = None


class ZWaveGenericFingerprint(BaseModel):
    genericType: Optional[ZWaveGenericType] = None
    specificType: Optional[List[ZWaveSpecificType]] = Field(
        None, description='List of reported command classes'
    )
    commandClasses: Optional[CommandClasses] = Field(
        None, description='List of CommandClasses to match on'
    )
    deviceIntegrationProfileKey: Optional[DeviceIntegrationProfileKey] = None


class Clusters(BaseModel):
    client: Optional[ClientClusters] = None
    server: Optional[ServerClusters] = None


class BasicChannel(BaseModel):
    name: Optional[str] = Field(None, description='Name of the channel')
    description: Optional[str] = Field(None, description='Description of the channel')
    type: Optional[ChannelType] = None
    termsOfServiceUrl: Optional[str] = Field(
        None,
        description='URL for a developer-provided Terms of Service agreement for the channel',
    )


class OrganizationUpdateRequest(BaseModel):
    label: Optional[Label] = None
    warehouseGroupId: Optional[WarehouseGroupId] = None
    mnId: Optional[MnId] = None


class InviteRequestItem(BaseModel):
    email: Email
    role: Role


class InviteResponseItem(InviteRequestItem):
    status: int = Field(
        ..., description='Status code for this invite entry.', example=200
    )
    info: str = Field(
        ..., description='Information on the individual invitation.', example='Success'
    )
    inviteId: Optional[str] = Field(
        None, description='Invite ID for sucessfully created invitations.'
    )
    acceptUrl: Optional[str] = Field(
        None,
        description='The URL the invitee can follow to accept a successful invitation (they must be logged in).',
    )


class OrganizationMemberRole(OrganizationMember):
    role: Optional[Role] = None


class ModifyMemberItem(BaseModel):
    member: OrganizationMember
    modification: Modification
    role: Optional[Role] = None


class Device(BaseModel):
    deviceId: DeviceId
    name: Optional[str] = Field(
        None,
        description='The name that the Device integration (Device Handler or SmartApp) defines for the Device.',
        example='color.light.100x',
    )
    label: Optional[str] = Field(
        None,
        description='The name that a user chooses for the Device. This defaults to the same value as name.',
        example='color.light.100x',
    )
    manufacturerName: str = Field(
        ..., description='The Device manufacturer name.', example='SmartThings'
    )
    presentationId: str = Field(
        ...,
        description='A non-unique id that is used to help drive UI information.',
        example='VD-STV_2018_K',
    )
    deviceManufacturerCode: Optional[str] = Field(
        None, description='The Device manufacturer code.', example='010F-0B01-2002'
    )
    locationId: Optional[str] = Field(
        None,
        description='The ID of the Location with which the Device is associated.',
        example='0c0b935d-0616-4441-a0bf-da7aeec3dc0a',
    )
    ownerId: Optional[str] = Field(
        None,
        description='The identifier for the owner of the Device instance.',
        example='1c75f712-2c3e-4e51-970c-a42ae7aedbdc',
    )
    roomId: Optional[str] = Field(
        None,
        description='The ID of the Room with which the Device is associated. If the Device is not associated with any room, this field will be null.',
        example='0fd2b1ef-1b33-4a54-9153-65aca91e9660',
    )
    deviceTypeId: Optional[str] = Field(
        None,
        description='Deprecated please look under "dth".',
        example='Deprecated please look under "dth".',
    )
    deviceTypeName: Optional[str] = Field(
        None,
        description='Deprecated please look under "dth".',
        example='Deprecated please look under "dth".',
    )
    deviceNetworkType: Optional[str] = Field(
        None,
        description='Deprecated please look under "dth".',
        example='Deprecated please look under "dth".',
    )
    components: Optional[List[DeviceComponent]] = Field(
        None, description='The IDs of all compenents on the Device.'
    )
    createTime: Optional[str] = Field(
        None, description='The time when the device was created at.'
    )
    parentDeviceId: Optional[str] = Field(
        None, description='The id of the Parent device.'
    )
    childDevices: Optional[List[Device]] = Field(
        None, description='Device details for all child devices of the Device.'
    )
    profile: Optional[DeviceProfileReference] = None
    app: Optional[AppDeviceDetails] = Field(
        None,
        description='Device Profile information for the SmartApp. This field will be empty if device type is not ENDPOINT_APP.',
    )
    ble: Optional[BleDeviceDetails] = Field(
        None,
        description='Bluetooth device information. This field will be empty if device type is not BLE.',
    )
    bleD2D: Optional[BleD2DDeviceDetails] = Field(
        None,
        description='Bluetooth device to device information. This field will be empty if device type is not BLE_D2D.',
    )
    dth: Optional[DthDeviceDetails] = Field(
        None,
        description='Device Profile information for DTH. This field will be empty if device type is not DTH.',
    )
    lan: Optional[LanDeviceDetails] = None
    zigbee: Optional[ZigbeeDeviceDetails] = None
    zwave: Optional[ZwaveDeviceDetails] = None
    matter: Optional[MatterDeviceDetails] = None
    ir: Optional[IrDeviceDetails] = Field(
        None,
        description='IR device information. This field will be empty if device type is not IR.',
    )
    irOcf: Optional[IrDeviceDetails] = Field(
        None,
        description='IR_OCF device information. This field will be empty if device type is not IR_OCF.',
    )
    ocf: Optional[OcfDeviceDetails] = Field(
        None,
        description='OCF device information. This field will be empty if device type is not OCF.',
    )
    viper: Optional[ViperDeviceDetails] = Field(
        None,
        description='Viper device information. This field will be empty if device type is not VIPER.',
    )
    type: DeviceIntegrationType
    restrictionTier: int = Field(
        ..., description='Restriction tier of the device, if any.'
    )


class PagedDevices(BaseModel):
    items: Optional[List[Device]] = None
    _links: Optional[Links] = None


class DeviceCommandsResponse(BaseModel):
    results: Optional[List[CommandResult]] = None


class DeviceProfileResponse(BaseModel):
    id: Optional[str] = Field(None, example='a362ddb6-349b-4650-9911-681b51069a57')
    name: Optional[str] = Field(None, example='thermostat1.model1')
    components: Optional[List[DeviceComponent]] = None
    metadata: Optional[DeviceProfileMetadata] = None
    status: Optional[DeviceProfileStatus] = None
    preferences: Optional[List[PreferenceResponse]] = None


class PagedDeviceProfiles(BaseModel):
    items: Optional[List[DeviceProfileResponse]] = None
    _links: Optional[Links] = None


class UpdateDeviceProfileRequest(BaseModel):
    components: Optional[List[DeviceComponentReference]] = Field(
        None,
        description='A list of `[ 1..20 ]` components for this profile.',
        max_items=20,
        min_items=1,
    )
    metadata: Optional[DeviceProfileMetadata] = None
    preferences: Optional[List[PreferenceRequest]] = Field(
        None,
        description='A list of preferences for this profile, whether implicit or explicit.',
    )


class CreateDeviceProfileRequest(BaseModel):
    name: constr(min_length=1, max_length=100) = Field(
        ..., description='A name for the device profile.', example='thermostat1.model1'
    )
    components: List[DeviceComponentReference] = Field(
        ...,
        description='A list of components for this profile. Exactly 1 component ID must be `main`.',
        max_items=20,
        min_items=1,
    )
    preferences: Optional[List[PreferenceRequest]] = Field(
        None,
        description='A list of preferences for this profile, whether implicit or explicit.',
    )
    metadata: Optional[DeviceProfileMetadata] = None


class PagedLocation(BaseModel):
    locationId: Optional[UUID] = Field(None, description='The ID of the location.')
    name: Optional[str] = Field(
        None, description='A name given for the location (eg. Home)'
    )
    parent: Optional[LocationParent] = None


class Location(BaseModel):
    locationId: Optional[UUID] = Field(None, description='The ID of the location.')
    name: Optional[str] = Field(
        None, description='A name given for the location (eg. Home)'
    )
    countryCode: Optional[str] = Field(
        None, description='An ISO Alpha-3 country code.  (i.e. GBR, USA)', example='USA'
    )
    latitude: Optional[float] = Field(None, description='A geographical latitude.')
    longitude: Optional[float] = Field(None, description='A geographical longitude.')
    regionRadius: Optional[int] = Field(
        None,
        description='The radius in meters around latitude and longitude which defines this location.',
    )
    temperatureScale: Optional[str] = Field(
        None,
        description='The desired temperature scale used within location. Value can be F or C.',
    )
    timeZoneId: Optional[str] = Field(
        None,
        description='An ID matching the Java Time Zone ID of the location. Automatically generated if latitude and longitude have been\nprovided.\n',
    )
    locale: Optional[str] = Field(
        None,
        description='We expect a POSIX locale but we also accept an IETF BCP 47 language tag.',
        example='en_US',
    )
    backgroundImage: Optional[str] = Field(None, description='Not currently in use.')
    additionalProperties: Optional[Dict[str, str]] = Field(
        None,
        description='Additional information about the location that allows SmartThings to further define your location.',
    )
    parent: Optional[LocationParent] = None
    created: Optional[datetime] = Field(
        None, description='The timestamp of when a location was created in UTC.'
    )
    lastModified: Optional[datetime] = Field(
        None, description='The timestamp of when a location was last updated in UTC.'
    )


class CreateLocationRequest(BaseModel):
    name: constr(min_length=1, max_length=40) = Field(
        ..., description='A name given to the Location (e.g. Home)'
    )
    countryCode: str = Field(
        ..., description='An ISO Alpha-3 country code (e.g. GBR, USA)'
    )
    latitude: Optional[float] = Field(None, description='A geographical latitude.')
    longitude: Optional[float] = Field(None, description='A geographical longitude.')
    regionRadius: Optional[int] = Field(
        None,
        description='The radius in meters around latitude and longitude which defines this Location.',
    )
    temperatureScale: Optional[str] = Field(
        None,
        description='The desired temperature scale used for the Location. Values include F and C.',
    )
    locale: Optional[str] = Field(
        None,
        description='We expect a POSIX locale but we also accept an IETF BCP 47 language tag.',
        example='en_US',
    )
    additionalProperties: Optional[Dict[str, str]] = Field(
        None,
        description='Additional information about the Location that allows SmartThings to further define your Location.',
    )
    parent: Optional[LocationParent] = None


class DeliveryMethods(BaseModel):
    __root__: List[Delivery]


class InstalledApp(BaseModel):
    installedAppId: UUID = Field(..., description='The ID of the installed app.')
    installedAppType: InstalledAppType
    installedAppStatus: InstalledAppStatus
    displayName: Optional[constr(max_length=100)] = Field(
        None, description='A user defined name for the installed app. May be null.'
    )
    appId: str = Field(..., description='The ID of the app.')
    referenceId: Optional[str] = Field(
        None,
        description='A reference to an upstream system.  For example, Behaviors would reference the behaviorId. May be null.\n',
    )
    locationId: Optional[UUID] = Field(
        None,
        description='The ID of the location to which the installed app may belong.',
    )
    owner: Owner
    notices: List[Notice]
    createdDate: datetime = Field(..., description='A UTC ISO-8601 Date-Time String')
    lastUpdatedDate: datetime = Field(
        ..., description='A UTC ISO-8601 Date-Time String'
    )
    ui: Optional[Ui] = Field(
        None,
        description='A collection of settings to drive user interface in SmartThings clients.  Currently, only applicable for\nLAMBDA_SMART_APP and WEBHOOK_SMART_APP app types.\n',
    )
    iconImage: Optional[IconImage] = Field(
        None,
        description='A default icon image for the app.',
        example={'url': 'https://smart-home-monitor.com/image'},
    )
    classifications: List[Classification] = Field(
        ...,
        description='An App maybe associated to many classifications.  A classification drives how the integration is presented\nto the user in the SmartThings mobile clients.  These classifications include:\n* AUTOMATION - Denotes an integration that should display under the "Automation" tab in mobile clients.\n* SERVICE - Denotes an integration that is classified as a "Service".\n* DEVICE - Denotes an integration that should display under the "Device" tab in mobile clients.\n* CONNECTED_SERVICE - Denotes an integration that should display under the "Connected Services" menu in mobile clients.\n* HIDDEN - Denotes an integration that should not display in mobile clients\n',
    )
    principalType: PrincipalType = Field(
        ...,
        description='Denotes the principal type to be used with the app.  Default is LOCATION.',
    )
    restrictionTier: Optional[int] = Field(
        None, description='Restriction tier of the install, if any.'
    )
    singleInstance: bool = Field(
        ...,
        description="Inform the installation systems that the associated app can only be installed once within a user's account.\n",
    )


class PagedInstalledApps(BaseModel):
    items: Optional[List[InstalledApp]] = None
    _links: Optional[Links] = None


class SubscriptionFilters(BaseModel):
    __root__: List[SubscriptionFilter] = Field(
        ..., description='An array of subscription filters'
    )


class PagedApps(BaseModel):
    items: Optional[List[PagedApp]] = None
    _links: Optional[Links] = None


class App1(BaseModel):
    appName: Optional[str] = Field(
        None,
        description='A user defined unique identifier for an app.  It is alpha-numeric, may contain dashes,\nunderscores, periods, and be less then 250 characters long.  It must be unique within your account.\n',
    )
    appId: Optional[UUID] = Field(
        None, description='A globally unique identifier for an app.'
    )
    appType: Optional[AppType] = None
    principalType: Optional[PrincipalTypeModel] = None
    classifications: Optional[List[AppClassification]] = Field(
        None,
        description='An App maybe associated to many classifications.  A classification drives how the integration is presented\nto the user in the SmartThings mobile clients.  These classifications include:\n* AUTOMATION - Denotes an integration that should display under the "Automation" tab in mobile clients.\n* SERVICE - Denotes an integration that is classified as a "Service".\n* DEVICE - Denotes an integration that should display under the "Device" tab in mobile clients.\n* CONNECTED_SERVICE - Denotes an integration that should display under the "Connected Services" menu in mobile clients.\n* HIDDEN - Denotes an integration that should not display in mobile clients\n',
    )
    displayName: Optional[constr(max_length=75)] = Field(
        None, description='A default display name for an app.\n'
    )
    description: Optional[constr(max_length=250)] = Field(
        None, description='A default description for an app.\n'
    )
    singleInstance: Optional[bool] = Field(
        False,
        description="Inform the installation systems that a particular app can only be installed once within a user's account.\n",
    )
    iconImage: Optional[IconImageModel] = None
    installMetadata: Optional[Dict[str, str]] = Field(
        None,
        description='System generated metadata that impacts eligibility requirements around installing an App.',
    )
    owner: Optional[Owner] = None
    createdDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )
    lastUpdatedDate: Optional[datetime] = Field(
        None, description='A UTC ISO-8601 Date-Time String'
    )
    lambdaSmartApp: Optional[LambdaSmartApp] = None
    webhookSmartApp: Optional[WebhookSmartApp] = None
    ui: Optional[AppUISettings] = None


class CreateAppResponse(BaseModel):
    app: Optional[App1] = None
    oauthClientId: Optional[UUID] = Field(None, description='The OAuth Client ID.')
    oauthClientSecret: Optional[UUID] = Field(
        None, description='The OAuth Client Secret.'
    )


class SceneCapability(BaseModel):
    capabilityId: Optional[str] = Field(None, description='The id of the capability')
    status: Optional[Status1] = Field(None, description='The status of the capability')
    commands: Optional[Dict[str, SceneCommand]] = Field(
        None, description='Capability commands'
    )


class CapabilityAttribute(BaseModel):
    schema_: Optional[AttributeSchema] = Field(None, alias='schema', description='')
    setter: Optional[str] = Field(
        None,
        description='The name of the command that sets this attribute',
        example='setColor',
    )
    enumCommands: Optional[List[EnumCommand]] = Field(
        None,
        description='a list of objects that specify which commands set this attribute',
        example=[{'command': 'on', 'value': 'on'}, {'command': 'off', 'value': 'off'}],
    )


class CreateCapabilityRequest(BaseModel):
    name: constr(regex=r'^[a-zA-Z0-9][a-zA-Z0-9 ]{1,35}$') = Field(
        ...,
        description='An alphanumeric English language name for the capability.',
        example='Color Temperature',
    )
    ephemeral: Optional[bool] = Field(False, example=True)
    attributes: Optional[Dict[str, CapabilityAttribute]] = Field(
        None,
        description='A mapping of attribute names to their definitions. All attribute names are lower camelcase. Required if no commands are specified.',
        example={
            'colorTemperature': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'value': {'type': 'integer', 'minimum': 1, 'maximum': 30000},
                        'unit': {'type': 'string', 'enum': ['K'], 'default': 'K'},
                    },
                    'additionalProperties': False,
                },
                'required': ['value'],
            }
        },
    )
    commands: Optional[Dict[str, CapabilityCommand]] = Field(
        None,
        description='A mapping of command names to their definitions. All command names are lower camelcase. Required if no attributes are specified.',
        example={
            'setColorTemperature': {
                'arguments': [
                    {
                        'name': 'temperature',
                        'optional': False,
                        'schema': {'type': 'integer', 'minimum': 1, 'maximum': 30000},
                    }
                ]
            }
        },
    )


class UpdateCapabilityRequest(BaseModel):
    attributes: Optional[Dict[str, CapabilityAttribute]] = Field(
        None,
        description='A mapping of attribute names to their definitions. All attribute names are lower camelcase.',
        example={
            'colorTemperature': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'value': {'type': 'integer', 'minimum': 1, 'maximum': 30000},
                        'unit': {'type': 'string', 'enum': ['K'], 'default': 'K'},
                    },
                    'additionalProperties': False,
                },
                'required': ['value'],
            }
        },
    )
    commands: Optional[Dict[str, CapabilityCommand]] = Field(
        None,
        description='A mapping of command names to their definitions. All command names are lower camelcase.',
        example={
            'setColorTemperature': {
                'arguments': [
                    {
                        'name': 'temperature',
                        'optional': False,
                        'schema': {'type': 'integer', 'minimum': 1, 'maximum': 30000},
                    }
                ]
            }
        },
    )


class UserIdApp(BaseModel):
    userId: Optional[str] = Field(None, description='UserId')
    endpointApps: Optional[List[EndpointApp]] = None


class Language(BaseModel):
    __root__: List[LanguageItem]


class Alternatives(BaseModel):
    __root__: List[AlternativeItem] = Field(
        ...,
        description='A collection of strings that can replace the attribute value in the `label` or `value`. Must be human-readable for the UI client to display.',
    )


class BadgeItem(BaseModel):
    iconUrl: IconUrl
    visibleConditions: Optional[List[VisibleCondition]] = None


class Icon(BaseModel):
    group: Optional[str] = 'main'
    iconUrl: Optional[IconUrl] = None
    badge: Optional[List[BadgeItem]] = None


class Icons(BaseModel):
    __root__: List[Icon]


class State2(BaseModel):
    label: Optional[FormattedLabel] = None
    unit: Optional[UnitModel] = None
    alternatives: Optional[Alternatives] = None


class StateItem(BaseModel):
    label: FormattedLabel
    alternatives: Optional[Alternatives] = None


class BasicPlusItem(BaseModel):
    displayType: DisplayType1 = Field(
        ...,
        description='To specify the type of UI component to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    stepper: Optional[Stepper] = None
    feature: Optional[Feature] = None
    visibleCondition: Optional[VisibleCondition] = None


class Command(BaseModel):
    name: Optional[str] = Field(
        None,
        description='name refers to command name and key of the alternatives is the argument of the command',
    )
    alternatives: Alternatives
    argumentType: Optional[ArgumentType] = None
    supportedValues: Optional[SupportedValues] = None


class State5(BaseModel):
    value: ValueModel
    valueType: Optional[ValueTypeModel] = None
    alternatives: Alternatives


class ListForDetailView(BaseModel):
    command: Command
    state: Optional[State5] = None


class ListBase(BaseModel):
    alternatives: Alternatives
    supportedValues: Optional[SupportedValues] = None


class ListForAutomationAction(ListBase):
    command: Optional[str] = Field(
        None,
        description='The name of the command that is called when an item is chosen from the list',
    )
    argumentType: Optional[ArgumentType] = None


class ListForAutomationCondition(ListBase):
    value: Optional[ValueModel] = None
    valueType: Optional[ValueTypeModel] = None


class State6(BaseModel):
    value: ValueModel
    valueType: Optional[ValueTypeModel] = None
    play: str = Field(
        ...,
        description='The value of "attribute" which indicates playing state. When the attribute value equals to this then UI will show playing state.',
    )
    pause: str = Field(
        ...,
        description='The value of "attribute" which indicates paused state. When the attribute value equals to this then UI will show paused state.',
    )
    alternatives: Optional[Alternatives] = None


class PlayPause(PlayPauseCommand):
    state: Optional[State6] = None


class State7(BaseModel):
    value: ValueModel
    play: str = Field(
        ...,
        description='The value of "attribute" which indicates playing state. When the attribute value equals to this then UI will show playing state.',
    )
    stop: str = Field(
        ...,
        description='The value of "attribute" which indicates stopped state. When the attribute value equals to this then UI will show stopped state.',
    )
    alternatives: Optional[Alternatives] = None
    valueType: Optional[ValueTypeModel] = None


class PlayStop(PlayStopCommand):
    state: State7


class Slider(SliderBase):
    command: Optional[str] = Field(
        None,
        description='The command which will send the value of the slider as an argument',
        example='setVolume',
    )
    argumentType: Optional[ArgumentType] = None
    value: Optional[ValueModel] = None
    valueType: Optional[ValueTypeModel] = None


class EnumSliderForAutomationCondition(BaseModel):
    alternatives: Alternatives
    value: ValueModel
    supportedOperators: Optional[List[SupportedOperator]] = None


class ListForArgument(ListBase):
    name: ArgumentName
    argumentType: Optional[ArgumentType] = None


class StatesArrayItem(StateItem, CapabilityKey):
    component: Component1
    visibleCondition: Optional[VisibleCondition] = None
    composite: Optional[Composite] = None
    group: Optional[Group] = None
    formatInfo: Optional[FormatInfo] = None


class BasicPlusArrayItem(BasicPlusItem, CapabilityKey):
    component: Optional[Component1] = None


class State8(BaseModel):
    value: ValueModel
    valueType: Optional[ValueTypeModel] = None
    on: str = Field(
        ..., description='The attribute value that corresponds to the `on` state.'
    )
    off: str = Field(
        ..., description='The attribute value that corresponds to the `off` state.'
    )
    label: Optional[FormattedLabel] = None
    alternatives: Optional[Alternatives] = None


class SwitchState(BaseModel):
    state: Optional[State8] = Field(
        None, description='To describe "on" and "off" state of a switch'
    )


class State9(BaseModel):
    value: Optional[ValueModel] = None
    on: str
    off: str
    valueType: Optional[ValueTypeModel] = None
    alternatives: Optional[Alternatives] = None


class SwitchStateForDashboard(BaseModel):
    state: Optional[State9] = Field(
        None, description='To describe "on" and "off" state of a switch'
    )


class SwitchForDashboard(SwitchCommand, SwitchStateForDashboard):
    pass


class StandbyPowerSwitchForDashboard(SwitchForDashboard):
    pass


class CapabilityValueForDashboardState(BaseModel):
    label: Optional[str] = None
    alternatives: Optional[Alternatives] = None


class DeviceConfigEntryForDashboardState(DeviceConfigEntryBase):
    idx: Optional[Idx] = None
    group: Optional[Group] = None
    values: Optional[List[CapabilityValueForDashboardState]] = Field(
        None,
        description='A list of valid values for the command argument or attribute that can override those defined by the alternatives provided in the capability presentation.',
        max_items=1,
    )
    composite: Optional[Composite] = None
    formatInfo: Optional[FormatInfo] = None


class DriverPermissions(BaseModel):
    __root__: List[DriverPermission] = Field(..., max_items=100, min_items=0)


class ZigbeeGenericFingerprint(BaseModel):
    clusters: Optional[Clusters] = None
    deviceIdentifiers: Optional[DeviceIdentifiers] = None
    zigbeeProfiles: Optional[ZigbeeProfiles] = None
    deviceIntegrationProfileKey: Optional[DeviceIntegrationProfileKey] = None


class OrganizationCreateRequest(OrganizationUpdateRequest):
    manufacturerName: Optional[ManufacturerName] = None
    name: OrganizationName


class PagedLocations(BaseModel):
    items: Optional[List[PagedLocation]] = None
    _links: Optional[Links] = None


class Invitation(BaseModel):
    invitationId: Optional[UUID] = Field(None, description='The ID of the invitation.')
    inviterUsername: Optional[str] = Field(
        None, description='The username for the inviter.'
    )
    entityType: Optional[EntityTypes] = None
    entityId: Optional[str] = Field(
        None,
        description='The identifier for the specific entity you are inviting access to.',
    )
    deliveryMethods: Optional[DeliveryMethods] = None
    status: Optional[StatusTypes] = None
    expiration: Optional[str] = Field(
        None,
        description='The IS0-8601 date time string in UTC for the expiration of an invitation.',
        example='2018-02-14T12:44:18+00:00',
    )


class SceneDeviceGroup(BaseModel):
    deviceGroupId: Optional[str] = Field(None, description='the id of the device')
    capability: Optional[SceneCapability] = None


class SceneDeviceGroupRequest(BaseModel):
    deviceGroupId: str = Field(..., description='the id of the device group')
    actionId: Optional[str] = Field(
        None,
        description='the id of the action to be created. Optional, sent by Reaver only',
    )
    capability: Optional[SceneCapability] = None


class SceneComponent(BaseModel):
    componentId: Optional[str] = Field(None, description='the id of the component')
    capabilities: Optional[List[SceneCapability]] = None


class Capability(BaseModel):
    id: str = Field(
        ...,
        description='A URL safe unique identifier for the capability.',
        example='namespace.colorTemperature',
    )
    version: int = Field(
        ..., description='The version number of the capability.', example=1
    )
    status: Status4 = Field(
        ...,
        description='The status of the capability.\n* __proposed__ - The capability is currently under development / in review.  The capability definition may go through changes, some of which may currently not function properly.\n* __live__ - The capability has been through review and the definition has been codified.  Once a definition transitions from proposed to live, it cannot be altered.\n* __deprecated__ - The capability is marked for removal in future versions.  It should only be used during a short period of time to allow for existing integrations and automations to continue to work while the transition to a newer definition is made.\n* __dead__ - A previously deprecated definition is now ready for removal.  Usage of the deprecated definition had dropped to a sufficiently low enough level to warrant removal.  The dead definition still exists but it can no longer be used or implemented by devices.\n',
    )
    name: str = Field(
        ...,
        description='An alphanumeric English language name for the capability.',
        example='Color Temperature',
    )
    ephemeral: Optional[bool] = Field(False, example=True)
    attributes: Optional[Dict[str, CapabilityAttribute]] = Field(
        None,
        description='A mapping of attribute names to their definitions. All attribute names are lower camelcase.',
        example={
            'colorTemperature': {
                'schema': {
                    'type': 'object',
                    'properties': {
                        'value': {'type': 'integer', 'minimum': 1, 'maximum': 30000},
                        'unit': {'type': 'string', 'enum': ['K'], 'default': 'K'},
                        'required': ['value'],
                    },
                }
            }
        },
    )
    commands: Optional[Dict[str, CapabilityCommand]] = Field(
        None,
        description='A mapping of command names to their definitions. All command names are lower camelcase.',
        example={
            'setColorTemperature': {
                'arguments': [
                    {
                        'name': 'temperature',
                        'schema': {'type': 'integer', 'minimum': 1, 'maximum': 30000},
                    }
                ]
            }
        },
    )


class Dashboard(BaseModel):
    states: Optional[List[DeviceConfigEntryForDashboardState]] = None
    actions: Optional[List[DeviceConfigEntryForDashboardAction]] = None
    groupVisibleConditions: Optional[GroupVisibleConditions] = None


class Dashboard1(BaseModel):
    states: Optional[List[DeviceConfigEntryForDashboardState]] = None
    actions: Optional[List[DeviceConfigEntryForDashboardAction]] = None
    groupVisibleConditions: Optional[GroupVisibleConditions] = None


class CapabilityValue(BaseModel):
    key: str = Field(
        ...,
        description='This can be either command name or attribute name.',
        example='thermostatMode.value',
    )
    enabledValues: Optional[List[str]] = Field(
        None,
        description='A list of values supported among those defined in the capability alternatives. For instance, a device may not support `auto` for supported thermostat fan modes, so this field might be an array containing `on` and `off`.',
        example=['cooling', 'heating'],
    )
    label: Optional[str] = None
    alternatives: Optional[Alternatives] = None
    range: Optional[Range] = None
    step: Optional[Step] = None


class Condition1(BaseModel):
    label: str = Field(..., example='Audio volume')
    displayType: DisplayType4 = Field(
        ...,
        description='Specify the type of UI component to use to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    slider: Optional[SliderForAutomationCondition] = None
    list: Optional[ListForAutomationCondition] = None
    numberField: Optional[NumberFieldForAutomationCondition] = None
    textField: Optional[TextFieldForAutomationCondition] = None
    enumSlider: Optional[EnumSliderForAutomationCondition] = None
    emphasis: Optional[bool] = Field(
        None,
        description='The effect used to emphasize this resource widget. The default value is false. If the emphasis value is true and this object has alternatives, a list will appear without a label',
    )


class AutomationCondition(CapabilityKey):
    label: str
    displayType: DisplayType6 = Field(
        ...,
        description='To specify the type of UI component to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    slider: Optional[SliderForAutomationCondition] = None
    list: Optional[ListForAutomationCondition] = None
    numberField: Optional[NumberFieldForAutomationCondition] = None
    textField: Optional[TextFieldForAutomationCondition] = None
    enumSlider: Optional[EnumSliderForAutomationCondition] = None
    emphasis: Optional[bool] = Field(
        None,
        description='The effect used to emphasize this resource widget. The default value is false. If the emphasis value is true and this object has alternatives, a list will appear without a label',
    )


class Switch(SwitchCommand, SwitchState):
    pass


class ToggleSwitch(Switch):
    pass


class Argument1(BaseModel):
    label: str = Field(..., example='Audio volume')
    displayType: DisplayType8 = Field(
        ...,
        description='Specify the type of UI component to use to display this action or state. The corresponding field must also be included. For example, if you specify "list" here, you must also include the "list" key and its object definition for this action or state.',
    )
    slider: Optional[SliderForArgument] = None
    list: Optional[ListForArgument] = None
    textField: Optional[TextFieldForArgument] = None
    numberField: Optional[NumberFieldForArgument] = None


class MultiArgCommand(BaseModel):
    command: str = Field(
        ..., description='Command name to trigger', example='playTrack'
    )
    arguments: List[Argument1]


class AutomationListItem(AutomationCondition):
    exclusion: Optional[List[ExcludedConditionItem]] = Field(
        None,
        description='To exclude specified automation in `exclude` when this item is selected by the user.',
    )
    component: Optional[Component1] = None
    visibleCondition: Optional[VisibleCondition] = None


class ToggleSwitchForDashboard(SwitchForDashboard):
    pass


class PagedDriver(BaseModel):
    driverId: DriverId
    name: DriverName
    packageKey: PackageKey
    deviceIntegrationProfiles: Optional[List[DeviceIntegrationProfileKey]] = Field(
        None, max_items=100, min_items=0
    )
    permissions: Optional[DriverPermissions] = None
    version: Optional[DriverVersion] = None


class DriverFingerprint(BaseModel):
    id: FingerprintId
    type: FingerprintType
    deviceLabel: Optional[FingerprintDeviceLabel] = None
    zigbeeGeneric: Optional[ZigbeeGenericFingerprint] = None
    zigbeeManfacturer: Optional[ZigbeeManufacturerFingerprint] = None
    zwaveManufacturer: Optional[ZWaveManufacturerFingerprint] = None
    zwaveGeneric: Optional[ZWaveGenericFingerprint] = None


class PagedDrivers(BaseModel):
    items: List[PagedDriver]
    _links: Links


class OrganizationResponse(OrganizationCreateRequest):
    developerGroupId: Optional[str] = Field(
        None, description='The user group for organization developers.'
    )
    adminGroupId: Optional[str] = Field(
        None, description='The user group for organization admins.'
    )
    organizationId: UUID = Field(
        ..., description='A generated UUID for an organization.'
    )
    isDefaultUserOrg: Optional[bool] = Field(
        False,
        description='Denotes whether this is the default user org for the caller.',
    )


class SceneDevice(BaseModel):
    deviceId: Optional[str] = Field(None, description='the id of the device')
    deviceLabel: Optional[str] = Field(None, description='the label of the device')
    deviceName: Optional[str] = Field(None, description='the name of the device')
    deviceTypeId: Optional[str] = Field(
        None, description="The identifier for the device's DeviceType."
    )
    components: Optional[List[SceneComponent]] = None
    locationId: Optional[str] = Field(None, description='Location of the device')


class SceneDeviceRequest(BaseModel):
    deviceId: Optional[str] = Field(None, description='the id of the device')
    actionId: Optional[str] = Field(
        None,
        description='the id of the action to be created. Optional, sent by Reaver only',
    )
    components: Optional[List[SceneComponent]] = None


class DeviceConfigEntry(DeviceConfigEntryBase):
    values: Optional[List[CapabilityValue]] = Field(
        None,
        description='A list of valid values for the command argument or attribute that can override those defined by the alternatives provided in the capability presentation.',
    )
    patch: Optional[List[PatchItem]] = Field(
        None,
        description='A format which is applied some operations(add / replace / remove) from the rfc6902(https://tools.ietf.org/html/rfc6902#section-4). Please note that array in the patch is sequentially processed.',
    )


class ExcludedDeviceActionConfigEntry(DeviceConfigEntry):
    exclusion: Optional[List[ExcludedActionItemId]] = Field(
        None,
        description='To exclude specified automation in `exclude` when this item is selected by the user.',
    )


class ExcludedDeviceConditionConfigEntry(DeviceConfigEntry):
    exclusion: Optional[List[ExcludedConditionItemId]] = Field(
        None,
        description='To exclude specified automation in `exclude` when this item is selected by the user.',
    )


class ActionItem(BaseModel):
    displayType: DisplayType = Field(
        ...,
        description='To specify the type of UI component to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    pushButton: Optional[PushButton] = None
    toggleSwitch: Optional[ToggleSwitchForDashboard] = None
    switch: Optional[SwitchForDashboard] = None
    standbyPowerSwitch: Optional[StandbyPowerSwitchForDashboard] = None
    statelessPowerToggle: Optional[StatelessPowerToggleForDashboard] = None
    playPause: Optional[PlayPause] = None
    playStop: Optional[PlayStop] = None
    group: Optional[Group] = None


class Action1(BaseModel):
    label: str = Field(..., example='Audio volume')
    displayType: DisplayType5 = Field(
        ...,
        description='To specify the type of UI component to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    slider: Optional[SliderForAutomationAction] = None
    list: Optional[ListForAutomationAction] = None
    textField: Optional[TextFieldForAutomationAction] = None
    numberField: Optional[NumberFieldForAutomationAction] = None
    multiArgCommand: Optional[MultiArgCommand] = None
    emphasis: Optional[bool] = Field(
        None,
        description='The effect used to emphasize this resource widget. The default value is false. If the emphasis value is true and this object has alternatives, a list will appear without a label',
    )


class AutomationForCapability(BaseModel):
    conditions: Optional[List[Condition1]] = Field(
        None,
        description='To specify the conditions of device state to trigger actions in the automation view of SmartThings app.',
    )
    actions: Optional[List[Action1]] = Field(
        None,
        description='To specify the actions of device control based on the device state in the automation view of SmartThings app.',
    )


class AutomationAction(CapabilityKey):
    label: str
    displayType: DisplayType7 = Field(
        ...,
        description='To specify the type of UI component to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    slider: Optional[SliderForAutomationAction] = None
    list: Optional[ListForAutomationAction] = None
    textField: Optional[TextFieldForAutomationAction] = None
    numberField: Optional[NumberFieldForAutomationAction] = None
    multiArgCommand: Optional[MultiArgCommand] = None
    emphasis: Optional[bool] = Field(
        None,
        description='The effect used to emphasize this resource widget. The default value is false. If the emphasis value is true and this object has alternatives, a list will appear without a label',
    )


class StandbyPowerSwitch(Switch):
    pass


class ActionsArrayItem(ActionItem, CapabilityKey):
    component: Optional[Component1] = None
    visibleCondition: Optional[VisibleCondition] = None
    group: Optional[Group] = None


class ActionListItem(AutomationAction):
    component: Optional[Component1] = None
    visibleCondition: Optional[VisibleCondition] = None
    exclusion: Optional[List[ExcludedActionItem]] = Field(
        None,
        description='To exclude specified automation in `exclude` when this item is selected by the user.',
    )


class Driver(PagedDriver):
    fingerprints: Optional[List[DriverFingerprint]] = Field(
        None, max_items=100, min_items=0
    )
    permissions: Optional[List[DriverPermission]] = Field(
        None, max_items=100, min_items=0
    )


class SceneAction(BaseModel):
    deviceRequest: Optional[SceneDeviceRequest] = None
    modeRequest: Optional[SceneModeRequest] = None
    sleepRequest: Optional[SceneSleepRequest] = None
    deviceGroupRequest: Optional[SceneDeviceGroupRequest] = None


class Automation(BaseModel):
    conditions: Optional[List[ExcludedDeviceConditionConfigEntry]] = None
    actions: Optional[List[ExcludedDeviceActionConfigEntry]] = None


class CreateProfileDeviceConfigRequest(BaseModel):
    iconUrl: Optional[IconUrl] = None
    dashboard: Optional[Dashboard] = None
    detailView: Optional[List[DeviceConfigEntry]] = None
    automation: Optional[Automation] = None


class Automation1(BaseModel):
    conditions: Optional[List[ExcludedDeviceConditionConfigEntry]] = None
    actions: Optional[List[ExcludedDeviceActionConfigEntry]] = None


class DeviceConfiguration(BaseModel):
    mnmn: Mnmn
    vid: Vid
    version: Optional[str] = Field(
        '0.0.1', description='The version of the device configuration.', example='0.0.1'
    )
    type: Optional[Type4] = 'profile'
    dpInfo: Optional[DpInfo] = None
    iconUrl: Optional[IconUrl] = None
    icons: Optional[Icons] = None
    dashboard: Optional[Dashboard1] = None
    detailView: Optional[List[DeviceConfigEntry]] = None
    automation: Optional[Automation1] = None


class PublicDeviceConfiguration(DeviceConfiguration):
    presentationId: Optional[str] = Field(
        None,
        description='System generated identifier that corresponds to a device presentation (formerly `vid`)',
    )
    manufacturerName: Optional[str] = Field(
        None,
        description='Secondary namespacing key for grouping presentations (formerly `mnmn`)',
    )


class DashboardModel(BaseModel):
    states: Optional[List[StatesArrayItem]] = None
    actions: Optional[List[ActionsArrayItem]] = None
    basicPlus: Optional[List[BasicPlusArrayItem]] = None
    groupVisibleConditions: Optional[GroupVisibleConditions] = None


class DashboardForCapability(BaseModel):
    states: Optional[List[StateItem]] = None
    actions: Optional[List[ActionItem]] = None
    basicPlus: Optional[List[BasicPlusItem]] = None


class DetailViewForCapabilityItem(BaseModel):
    label: str = Field(..., example='Front door')
    displayType: DisplayType2 = Field(
        ...,
        description='To specify the type of UI component to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    toggleSwitch: Optional[ToggleSwitch] = None
    standbyPowerSwitch: Optional[StandbyPowerSwitch] = None
    switch: Optional[Switch] = None
    slider: Optional[Slider] = None
    pushButton: Optional[PushButton] = None
    textButton: Optional[TextButton] = None
    playPause: Optional[PlayPause] = None
    playStop: Optional[PlayStop] = None
    list: Optional[ListForDetailView] = None
    textField: Optional[TextField] = None
    numberField: Optional[NumberField] = None
    stepper: Optional[Stepper] = None
    state: Optional[State2] = None


class DetailViewForCapability(BaseModel):
    __root__: List[DetailViewForCapabilityItem]


class DetailViewItem(CapabilityKey):
    label: str
    displayType: DisplayType3 = Field(
        ...,
        description='To specify the type of UI component to display this action or state. The corresponding field must also be included. For example, if you specify "switch" here, you must also include the "switch" key and its object definition for this action or state.',
    )
    toggleSwitch: Optional[ToggleSwitch] = None
    standbyPowerSwitch: Optional[StandbyPowerSwitch] = None
    switch: Optional[Switch] = None
    slider: Optional[Slider] = None
    pushButton: Optional[PushButton] = None
    textButton: Optional[TextButton] = None
    playPause: Optional[PlayPause] = None
    playStop: Optional[PlayStop] = None
    list: Optional[ListForDetailView] = None
    textField: Optional[TextField] = None
    numberField: Optional[NumberField] = None
    stepper: Optional[Stepper] = None
    state: Optional[State2] = None
    multiArgCommand: Optional[MultiArgCommand] = None


class AutomationModel(BaseModel):
    conditions: Optional[List[AutomationListItem]] = Field(
        None,
        description='To specify the conditions of device state to trigger actions in the automation view of SmartThings app.',
    )
    actions: Optional[List[ActionListItem]] = Field(
        None,
        description='To specify the actions of device control based on the device state in the automation view of SmartThings app.',
    )


class DetailViewListItem(DetailViewItem):
    component: Optional[Component1] = None
    visibleCondition: Optional[VisibleCondition] = None


class SceneActionSequence(BaseModel):
    __root__: List[SceneAction]


class CreateDeviceConfigRequest(CreateProfileDeviceConfigRequest, DeviceConfigType):
    pass


class CapabilityPresentationForPUT(BaseModel):
    dashboard: Optional[DashboardForCapability] = None
    detailView: Optional[DetailViewForCapability] = None
    automation: Optional[AutomationForCapability] = None


class CapabilityPresentation(CapabilityPresentationForPUT):
    id: Optional[str] = Field(None, example='audioVolume')
    version: Optional[Version] = Field(None, example=1)


class DetailView(BaseModel):
    __root__: List[DetailViewListItem]


class SceneRequest(BaseModel):
    sceneName: str = Field(..., description='The user-defined name of the Scene')
    sceneIcon: Optional[str] = Field(None, description='The name of the icon')
    sceneColor: Optional[str] = Field(None, description='The color of the icon')
    devices: List[SceneDeviceRequest] = Field(
        ..., description='Non-sequential list of device actions'
    )
    sequences: Optional[List[SceneActionSequence]] = Field(
        None, description='List of parallel action sequences'
    )
    mode: Optional[SceneModeRequest] = None
    securityMode: Optional[SceneSecurityModeRequest] = None
    devicegroups: Optional[List[SceneDeviceGroupRequest]] = Field(
        None, description='List of device group actions'
    )


class CreateCapabilityPresentationRequest(CapabilityPresentationForPUT):
    id: str
    version: Version


class DevicePresentation(BaseModel):
    mnmn: Mnmn
    vid: Vid
    version: Optional[str] = Field(
        '0.0.1', description='The version of the device presentation.', example='0.0.1'
    )
    iconUrl: Optional[IconUrl] = None
    icons: Optional[Icons] = None
    dashboard: Optional[DashboardModel] = None
    detailView: Optional[DetailView] = None
    automation: Optional[AutomationModel] = None
    dpInfo: DpInfo
    language: Optional[Language] = None


class DossierDevicePresentation(DevicePresentation):
    manufacturerName: Optional[str] = Field(
        None,
        description='Secondary namespacing key for grouping presentations (formerly `mnmn`)',
    )
    presentationId: Optional[str] = Field(
        None,
        description='System generated identifier that corresponds to a device presentation (formerly `vid`)',
    )


class RuleRequest(BaseModel):
    name: str = Field(..., description='The name for the Rule')
    actions: List[Action]
    sequence: Optional[ActionSequence] = Field(
        None,
        description='The sequence in which the actions are to be executed (i.e. Serial (default) or Parallel).',
    )
    timeZoneId: Optional[str] = Field(
        None,
        description='The time zone ID for this Rule. This overrides the Location time zone ID, but is overridden by time zone ID provided by each operand individually.',
    )


class Action(BaseModel):
    if_: Optional[IfAction] = Field(None, alias='if')
    sleep: Optional[SleepAction] = None
    command: Optional[CommandAction] = None
    every: Optional[EveryAction] = None
    location: Optional[LocationAction] = None


class SleepAction(BaseModel):
    duration: Interval


class EveryAction(BaseModel):
    interval: Optional[Interval] = None
    specific: Optional[DateTimeOperand] = None
    actions: List[Action]
    sequence: Optional[ActionSequence] = Field(
        None,
        description='The sequence in which the actions are to be executed i.e. Serial (default) or Parallel',
    )


class BasicCondition(BaseModel):
    and_: Optional[List[Condition]] = Field(None, alias='and')
    or_: Optional[List[Condition]] = Field(None, alias='or')
    not_: Optional[Condition] = Field(None, alias='not')
    equals: Optional[EqualsCondition] = None
    greaterThan: Optional[GreaterThanCondition] = None
    greaterThanOrEquals: Optional[GreaterThanOrEqualsCondition] = None
    lessThan: Optional[LessThanCondition] = None
    lessThanOrEquals: Optional[LessThanOrEqualsCondition] = None
    between: Optional[BetweenCondition] = None


class Condition(BaseModel):
    and_: Optional[List[Condition]] = Field(None, alias='and')
    or_: Optional[List[Condition]] = Field(None, alias='or')
    not_: Optional[Condition] = Field(None, alias='not')
    equals: Optional[EqualsCondition] = None
    greaterThan: Optional[GreaterThanCondition] = None
    greaterThanOrEquals: Optional[GreaterThanOrEqualsCondition] = None
    lessThan: Optional[LessThanCondition] = None
    lessThanOrEquals: Optional[LessThanOrEqualsCondition] = None
    between: Optional[BetweenCondition] = None
    changes: Optional[ChangesCondition] = None
    remains: Optional[RemainsCondition] = None
    was: Optional[WasCondition] = None


class SimpleCondition(BaseModel):
    left: Operand
    right: Operand
    aggregation: Optional[ConditionAggregationMode] = None


class BetweenCondition(BaseModel):
    value: Operand
    start: Operand
    end: Operand
    aggregation: Optional[ConditionAggregationMode] = None


class Operand(BaseModel):
    boolean: Optional[bool] = None
    decimal: Optional[float] = None
    integer: Optional[int] = None
    string: Optional[str] = None
    array: Optional[ArrayOperand] = None
    map: Optional[MapOperand] = None
    device: Optional[DeviceOperand] = None
    location: Optional[LocationOperand] = None
    date: Optional[DateOperand] = None
    time: Optional[TimeOperand] = None
    datetime: Optional[DateTimeOperand] = None


class ArrayOperand(BaseModel):
    operands: List[Operand]
    aggregation: Optional[OperandAggregationMode] = None


class DateTimeOperand(BaseModel):
    timeZoneId: Optional[str] = Field(None, description='A java time zone ID reference')
    locationId: Optional[str] = Field(
        None, description='Location ID for location actions'
    )
    daysOfWeek: Optional[List[DayOfWeek]] = None
    year: Optional[int] = None
    month: Optional[conint(ge=1, le=12)] = None
    day: Optional[conint(ge=1, le=31)] = None
    reference: TimeReference
    offset: Optional[Interval] = None


class TimeOperand(BaseModel):
    timeZoneId: Optional[str] = Field(None, description='A java time zone ID reference')
    daysOfWeek: Optional[List[DayOfWeek]] = None
    reference: TimeReference
    offset: Optional[Interval] = None


class Interval(BaseModel):
    value: Operand
    unit: IntervalUnit


class PagedRules(BaseModel):
    items: Optional[List[Rule]] = None
    _links: Optional[Links] = None


class Rule(RuleRequest):
    id: str = Field(..., description='Unique id for the Rule')
    status: Optional[Status] = Field('Enabled', description='The status of the Rule')
    executionLocation: Optional[ExecutionLocation] = Field(
        None,
        description='The location where the rule is executing, either local or cloud',
    )
    ownerId: str = Field(..., description='Owner id')
    ownerType: OwnerType1 = Field(
        ..., description='The owner of the rule is either a location or user'
    )
    creator: Optional[Creator] = None
    dateCreated: str = Field(..., description='Created date time')
    dateUpdated: str = Field(..., description='Last updated date time')


class ChangesCondition(BasicCondition):
    id: str = Field(..., description='Unique id for the condition')
    operand: Optional[Operand] = None


class RemainsCondition(BasicCondition):
    id: str = Field(..., description='Unique id for the condition')
    operand: Optional[Operand] = None
    duration: Interval


class WasCondition(BasicCondition):
    id: str = Field(..., description='Unique id for the condition')
    duration: Interval
    operand: Optional[Operand] = None


class IfAction(Condition):
    then: Optional[List[Action]] = None
    else_: Optional[List[Action]] = Field(None, alias='else')
    sequence: Optional[IfActionSequence] = Field(
        None, description='The sequence in which the actions are to be executed'
    )


class EqualsCondition(SimpleCondition):
    pass


class GreaterThanCondition(SimpleCondition):
    pass


class GreaterThanOrEqualsCondition(SimpleCondition):
    pass


class LessThanCondition(SimpleCondition):
    pass


class LessThanOrEqualsCondition(SimpleCondition):
    pass

class NotificationType(Enum):
    ALERT = 'ALERT'

class NotificationRequest(BaseModel):
    locationId: Optional[str] = None
    type:       NotificationType
    title:      str
    message:    str

Error.update_forward_refs()
IrDeviceDetails.update_forward_refs()
InstalledAppLifecycleError.update_forward_refs()
Device.update_forward_refs()
RuleRequest.update_forward_refs()
Action.update_forward_refs()
SleepAction.update_forward_refs()
EveryAction.update_forward_refs()
BasicCondition.update_forward_refs()
Condition.update_forward_refs()
SimpleCondition.update_forward_refs()
BetweenCondition.update_forward_refs()
Operand.update_forward_refs()
DateTimeOperand.update_forward_refs()
TimeOperand.update_forward_refs()
PagedRules.update_forward_refs()
