from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Extra, Field, conint, constr

from smartapp.api.models import smartthings

class LifecycleType(Enum):
    configuration   = 'CONFIGURATION'
    install         = 'INSTALL'
    update          = 'UPDATE'
    event           = 'EVENT'
    oauth_callback  = 'OAUTH_CALLBACK'
    uninstall       = 'UNINSTALL'

class SubscriptionType(Enum):
    DEVICE             = 'DEVICE'
    CAPABILITY         = 'CAPABILITY'
    MODE               = 'MODE'
    DEVICE_LIFECYCLE   = 'DEVICE_LIFECYCLE'
    DEVICE_HEALTH      = 'DEVICE_HEALTH'
    SECURITY_ARM_STATE = 'SECURITY_ARM_STATE'
    HUB_HEALTH         = 'HUB_HEALTH'
    SCENE_LIFECYCLE    = 'SCENE_LIFECYCLE'

class EventType(Enum):
    DEVICE_COMMANDS_EVENT         = 'DEVICE_COMMANDS_EVENT'
    DEVICE_EVENT                  = 'DEVICE_EVENT'
    DEVICE_HEALTH_EVENT           = 'DEVICE_HEALTH_EVENT'
    DEVICE_LIFECYCLE_EVENT        = 'DEVICE_LIFECYCLE_EVENT'
    HUB_HEALTH_EVENT              = 'HUB_HEALTH_EVENT'
    MODE_EVENT                    = 'MODE_EVENT'
    SCENE_LIFECYCLE_EVENT         = 'SCENE_LIFECYCLE_EVENT'
    SECURITY_ARM_STATE_EVENT      = 'SECURITY_ARM_STATE_EVENT'
    TIMER_EVENT                   = 'TIMER_EVENT'
    INSTALLED_APP_LIFECYCLE_EVENT = 'INSTALLED_APP_LIFECYCLE_EVENT'
    WEATHER_EVENT                 = 'WEATHER_EVENT'

class LifecycleBase(BaseModel):
    lifecycle:    str
    executionId:  Optional[str]
    locale:       Optional[str]
    version:      Optional[str]
    settings:     Optional[Dict]

class Phase(Enum):
    initialize = 'INITIALIZE'
    page       = 'PAGE'

class Settings(BaseModel):
    __root__: Dict[str, str]

class Option(BaseModel):
    id:   str
    name: str

Permissions  = List[str]
Capabilities = List[str]
Options      = List[Option]

class Subscription(smartthings.Subscription):
    pass

class UpdateEvent(smartthings.DeviceStateEvent):
    pass

class SettingType(Enum):
    TEXT       = 'TEXT'
    PARAGRAPH  = 'PARAGRAPH'
    DEVICE     = 'DEVICE'
    PERMISSION = 'PERMISSION'
    MODE       = 'MODE'
    SCENE      = 'SCENE'
    ENUM       = 'ENUM'
    MESSAGE    = 'MESSAGE'
    STRING     = 'STRING'
    PAGE       = 'PAGE'
    IMAGE      = 'IMAGE'
    NUMBER     = 'NUMBER'

class SmartAppEventRequest(smartthings.SmartAppEventRequest):
    pass

class InitializeData(BaseModel):
    name:           str
    description:    str
    id:             str
    permissions:    Permissions
    firstPageId:    str

class PageSetting(BaseModel):
    id:           str
    name:         str
    description:  Optional[str]
    type:         SettingType
    required:     bool
    multiple:     bool
    page:         Optional[str]
    image:        Optional[str]
    options:      Optional[Options]
    capabilities: Optional[Capabilities]
    permissions:  Optional[Permissions]
    defaultValue: Optional[str]

class PageSection(BaseModel):
    name: str
    settings: Optional[List[PageSetting]]

class PageData(BaseModel):
    pageId:         str
    name:           str
    nextPageId:     Optional[str]
    previousPageId: Optional[str]
    complete:       bool
    sections:       Optional[List[PageSection]]
    render_func:    Optional[Any] = Field(exclude=True)

class ConfigurationData(BaseModel):
    installedAppId: Optional[str]
    phase:          Optional[Phase]
    pageId:         Optional[str]
    previousPageId: Optional[str]
    config:         Optional[smartthings.ConfigMap]
    permissions:    Optional[List[str]]
    settings:       Optional[Settings]
    initialize:     Optional[InitializeData]
    page:           Optional[PageData]

class ConfirmationData(BaseModel):
    appId: str
    confirmationUrl: str

class InstalledApp(BaseModel):
    installedAppId: Optional[str]
    locationId:     Optional[str]
    config:         smartthings.ConfigMap
    permissions:    Optional[Permissions]
    settings:       Optional[Settings]

class InstallData(BaseModel):
    authToken:    Optional[str]
    refreshToken: Optional[str]
    installedApp: Optional[InstalledApp]

class UpdateData(BaseModel):
    authToken:           Optional[str]
    refreshToken:        Optional[str]
    installedApp:        Optional[InstalledApp]
    permissions:         Optional[Permissions]
    previousConfig:      Optional[smartthings.ConfigMap]
    previousPermissions: Optional[Permissions]

class Event(BaseModel):
    eventType:        smartthings.EventType
    deviceEvent:      Optional[smartthings.DeviceEvent]
    modeEvent:        Optional[smartthings.ModeEvent]
    deviceLifecycle:  Optional[smartthings.DeviceLifecycleEvent]
    sceneLifecycle:   Optional[smartthings.SceneLifecycleEvent]

class EventData(BaseModel):
    authToken:           Optional[str]
    installedApp:        Optional[InstalledApp]
    events:              Optional[List[Event]]

class OAuthCallbackData(BaseModel):
    installedAppId: str
    urlPath:        str

class UninstallData(BaseModel):
    installedApp: Optional[InstalledApp]
    settings:     Optional[Settings]

class PingData(BaseModel):
    challenge: str

class Install(LifecycleBase):
    installData: InstallData

class Configuration(LifecycleBase):
    configurationData: ConfigurationData

class Confirmation(LifecycleBase):
    confirmationData: ConfirmationData

class Update(LifecycleBase):
    updateData:   UpdateData
    settings:     Optional[Settings]

class DeviceEvent(BaseModel):
    deviceId: str
    event:    smartthings.DeviceStateEvent

class LifecycleResponse(BaseModel):
   targetUrl:          Optional[str]
   installData:        Optional[InstallData]
   updateData:         Optional[UpdateData]
   eventData:          Optional[EventData]
   oAuthCallbackData:  Optional[OAuthCallbackData]
   uninstallData:      Optional[UninstallData]
   configurationData:  Optional[ConfigurationData]
   confirmationData:   Optional[ConfirmationData]
   pingData:           Optional[PingData]

class RequestStatus(BaseModel):
    status:     str
