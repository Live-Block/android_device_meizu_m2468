#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.file import File
from extract_utils.fixups_blob import (
    BlobFixupCtx,
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/meizu/m2468',
    'hardware/qcom-caf/sm8550',
    'hardware/qcom-caf/wlan',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.diaghal@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
    ): lib_fixup_vendor_suffix,
    (
        'audio.primary.kalama',
        'libar-acdb',
        'libagmclient',
        'libagmmixer',
        'libats',
        'libagmmixer',
        'libar-gsl'
        'libar-gpr',
        'libpalclient',
        'liblx-ar_util',
        'liblx-osal',
        'libwifi-hal-ctrl',
        'libagm',
        'libar-pal',
        'libcodec2_hidl@1.0',
        'vendor.qti.hardware.pal@1.0-impl',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    (
        'product/etc/permissions/vendor.qti.hardware.data.connection-V1.0-java.xml',
        'product/etc/permissions/vendor.qti.hardware.data.connection-V1.1-java.xml',
        'product/etc/permissions/vendor.qti.hardware.data.connectionaidl-V1-java.xml'
    ): blob_fixup()
        .regex_replace('version="2.0"', 'version="1.0"'),

    (
        'vendor/lib64/libbluetooth_audio_session_aidl.so'
    )
    : blob_fixup()
        .replace_needed('android.hardware.bluetooth.audio-V2-ndk', 'android.hardware.bluetooth.audio-V5-ndk'),

        'vendor/lib64/hw/audio.bluetooth.default.so': blob_fixup()
        .replace_needed('android.hardware.bluetooth.audio-V2-ndk', 'android.hardware.bluetooth.audio-V5-ndk')
        .replace_needed('android.media.audio.common.types-V1-ndk', 'android.media.audio.common.types-V4-ndk'),

        'vendor/bin/hw/android.hardware.power-service': blob_fixup()
        .replace_needed('android.hardware.power-V3-ndk', 'android.hardware.power-V4-ndk'),

        'vendor/bin/hw/hostapd': blob_fixup()
        .add_needed('libcrypto-v33.so')
        .add_needed('libssl.so')
        .replace_needed('android.hardware.wifi.hostapd-V1-ndk', 'android.hardware.wifi.hostapd-V3-ndk'),

        'vendor/bin/hw/android.hardware.health-service.qti': blob_fixup()
        .add_needed('libbase_shim.so')
        .replace_needed('android.hardware.health-V1-ndk', 'android.hardware.health-V4-ndk'),

        'vendor/bin/rkp_factory_extraction_tool': blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so')
        .replace_needed('android.hardware.security.keymint-V2-ndk', 'android.hardware.security.keymint-V4-ndk'),

        'vendor/bin/hw/android.hardware.sensors-service.multihal': blob_fixup()
        .replace_needed('android.hardware.sensors-V1-ndk', 'android.hardware.sensors-V3-ndk'),

        'vendor/bin/hw/wpa_supplicant': blob_fixup()
        .replace_needed('android.hardware.wifi.supplicant-V1-ndk', 'android.hardware.wifi.supplicant-V4-ndk'),

    ( 
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/bin/hw/android.hardware.security.keymint-service-spu-qti',
        'vendor/lib64/libspukeymint.so',
        'vendor/lib64/libqtikeymint.so',
    ): blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so'),

        'vendor/lib64/libarcsoft_beautyshot.so': blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),

    (
        'vendor/lib64/nfc_nci.nqx.default.hw.so',
        'vendor/lib64/tms-utils.so',
        'vendor/lib64/nfc_nci.thn31nfc.tms.so',
    ): blob_fixup()
        .add_needed('libbase_shim.so'),

        'vendor/bin/slim_daemon': blob_fixup()
        .add_needed('libemutls_get_address.so'),

        'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),

        'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),

}  # fmt: skip

module = ExtractUtilsModule(
    'm2468',
    'meizu',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_firmware_proprietary_file=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()