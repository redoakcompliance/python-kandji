import importlib.metadata
import json

import requests


class Kandji:
    """Class for accessing the Kandji API.

    Attributes:
        api_url (str): Your organization’s API URL.
            EU Region: `https://SubDomain.clients.eu.kandji.io`
            US Region: `https://SubDomain.clients.us-1.kandji.io`
        api_token (str): API token.
    """

    version = importlib.metadata.version("kandji")

    def __init__(self, api_url, api_token):
        self.api_url = f"{api_url}/api/v1"
        self.headers = {
            "User-Agent": f"python-kandji/{self.version}",
            "Authorization": f"Bearer {api_token}",
        }

    def _request(self, method, path, **kwargs):
        uri = "{}{}".format(self.api_url, path)
        headers = kwargs.get("headers", self.headers)
        params = self._format_params(kwargs.get("params", {}))
        payload = kwargs.get("json", {})

        response = getattr(requests, method)(
            uri,
            headers=headers,
            params=params,
            json=payload,
        )

        if response.status_code != 200:
            return {"response": {"status": response.status_code}}

        if response.headers['Content-Type'] == "application/x-x509-ca-cert":
            return response.text

        return response.json()

    @staticmethod
    def _format_params(params):
        return {k: json.dumps(v) if isinstance(v, bool) else v for k, v in params.items()}

    def _get(self, path, **kwargs):
        return self._request("get", path, **kwargs)

    def _post(self, path, **kwargs):
        return self._request("post", path, **kwargs)

    def _patch(self, path, **kwargs):
        return self._request("patch", path, **kwargs)

    def _delete(self, path, **kwargs):
        return self._request("delete", path, **kwargs)

    def create_ade_integration(self, blueprint_id: str, phone: str, email: str, file: str):
        """Create ADE integration.

        This request will create a new ADE integration.

        The default `blueprint_id`, `phone` number, `email` address,and MDM server
        token `file` downloaded from ABM are required and must be sent in the request.

        Args:
            blueprint_id (str): Blueprint ID.
            phone (str): Phone number.
            email (str): Email address.
            file (str): This is the MDM server token file(.p7m) download from ABM.
                Once downloaded from ABM, the file can be uploaded via API.

        Returns:
            dict
        """
        headers = self.headers
        headers["Content-Type"] = "multipart/form-data"

        payload = {
            "blueprint_id": blueprint_id,
            "phone": phone,
            "email": email,
        }

        files = [("file", ("file", open(file, "rb"), "application/octet-stream"))]

        return self._post(
            "/integrations/apple/ade",
            headers=headers,
            json=payload,
            files=files,
        )

    def renew_ade_integration(self, ade_token_id: str, blueprint_id: str, phone: str, email: str, file: str):
        """Renew ADE integration.

        This request will renew an existing ADE integration.

        The default `blueprint_id`, `phone` number, `email` address, and MDM server token
        `file`from the associated MDM server in ABM are required and must be sent in the request.

        Args:
            ade_token_id (str): ADE Token ID.
            blueprint_id (str): Blueprint ID.
            phone (str): Phone number.
            email (str): Email address.
            file (str): This is the MDM server token file(.p7m) download from ABM.
                Once downloaded from ABM, the file can be uploaded via API.

        Returns:
            dict
        """
        headers = self.headers
        headers["Content-Type"] = "multipart/form-data"

        payload = {
            "blueprint_id": blueprint_id,
            "phone": phone,
            "email": email,
        }

        files = [("file", ("file", open(file, "rb"), "application/octet-stream"))]

        return self._post(
            f"/integrations/apple/ade/{ade_token_id}/renew",
            headers=headers,
            json=payload,
            files=files,
        )

    def update_ade_integration(self, ade_token_id: str, blueprint_id: str, phone: str, email: str):
        """Update ADE integration.

        This request will update the default blueprint, phone number,
        and email address in an existing ADE integration.

        The default `blueprint_id`, `phone` number, and `email` address
        must be sent in the request.

        Args:
            ade_token_id (str): ADE Token ID.
            blueprint_id (str): Blueprint ID.
            phone (str): Phone number.
            email (str): Email address.

        Returns:
            dict
        """
        payload = {
            "blueprint_id": blueprint_id,
            "phone": phone,
            "email": email,
        }

        return self._patch(f"/integrations/apple/ade/{ade_token_id}", json=payload)

    def delete_ade_integration(self, ade_token_id: str):
        """Delete ADE integration.

        WARNING!
        This is a HIGHLY destructive action.

        Deleting an ADE token will unassign the associated device records from Kandji.
        For currently enrolled devices that were assigned to Kandji via the delete ADE integration
        will not be impacted until they are wiped and reprovisioned. This action is essentially
        the same as removing an ADE token from MDM and then adding it back.

        If applicable, be sure to reassign the device records in ABM.

        Args:
            ade_token_id (str): ADE Token ID.

        Returns:
           None: This request doesn't return a response body
        """
        return self._delete(f"/integrations/apple/ade/{ade_token_id}")

    def list_ade_integrations(self):
        """List ADE integrations.

        This request returns a list of configured ADE integrations.

        Returns:
            dict
        """
        return self._get("/integrations/apple/ade")

    def list_ade_devices(self, ade_token_id: str, page: int = 1):
        """List devices associated to ADE token.

        This request returns a list of devices associated with a
        specified `ade_token_id` as well as their enrollment status.

        When the `mdm_device` key value is `null`, this can be taken
        as an indication that the device is awaiting enrollment into Kandji.

        When data is present within the mdm_device dictionary, you can
        reference the `device_id` as the ID of the enrolled device record.

        Args:
            ade_token_id (str): _Automated Device Enrollment token ID
            page (int, optional): Request a specific page. Defaults to 1.

        Returns:
            dict
        """
        params = {
            "page": page,
        }
        return self._get(f"/integrations/apple/ade/{ade_token_id}/devices", params=params)

    def get_ade_integration(self, ade_token_id: str):
        """Get ADE integration.

        This request returns a specific ADE integration based on the `ade_token_id` passed.

        Args:
            ade_token_id (str): Automated Device Enrollment token ID

        Returns:
            dict
        """
        return self._get(f"/integrations/apple/ade/{ade_token_id}")

    def get_ade_public_key(self):
        """Download ADE public key.

        This request returns the public key used to create an
        MDM server connection in Apple Business Manager.

        The encoded information needs to be saved to a file
        with the `.pem` format and then uploaded to ABM.

        Returns:
            str
        """
        return self._get("/integrations/apple/ade/public_key/")

    def list_blueprints(
        self,
        id: str = None,
        id__in: str = None,
        name: str = None,
        limit: int = None,
        offset: int = None,
    ):
        """This request returns a list of a blueprint records in the Kandji instance.

        Optional query parameters can be specified to filter the results.

        Args:
            id (str, optional): Look up a specific Blueprint by its ID
            id__in (str, optional): Specify a list of Blueprint IDs to limit the results to.
            name (str, optional): Return Blueprint names "containing" the specified search string.
            limit (int, optional): Number of results to return per page.
            offset (int, optional): The initial index from which to return the results.

        Returns:
            dict
        """
        params = {
            "id": id,
            "id__in": id__in,
            "name": name,
            "limit": limit,
            "offset": offset,
        }

        return self._get("/blueprints", params=params)

    def get_blueprint(self, id: str):
        """This request returns information about a specific blueprint based on blueprint ID.

        Args:
            id (str): Blueprint ID

        Returns:
            dict
        """
        return self._get(f"/blueprints/{id}")

    def get_blueprint_templates(self, limit: int = None, offset: int = None):
        """This request returns a list of a blueprint templates in the Kandji instance.

        Args:
            limit (int, optional): Number of results to return per page.
            offset (int, optional): The initial index from which to return the results.

        Returns:
            dict
        """
        params = {
            "limit": limit,
            "offset": offset,
        }

        return self._get("/blueprints/templates/", params=params)

    def list_devices(
        self,
        asset_tag: str = None,
        blueprint_id: str = None,
        device_id: str = None,
        device_name: str = None,
        mac_address: str = None,
        model: str = None,
        ordering: str = None,
        os_version: str = None,
        platform: str = None,
        serial_number: str = None,
        user: str = None,
        user_email: str = None,
        user_id: str = None,
        user_name: str = None,
        limit: int = 300,
        offset: int = None,
    ):
        """This request returns a list of devices in a Kandji tenant.

        Optional query parameters can be specified to filter the results.

        Args:
            asset_tag (str, optional): Asset tag.
            blueprint_id (str, optional): Blueprint ID.
            device_id (str, optional): Device ID.
            device_name (str, optional): Device name.
            mac_address (str, optional): MAC address.
            model (str, optional): Model string.
            ordering (str, optional): Response order.
                Possible values:
                `asset_tag`, `blueprint_id`, `device_id`, `device_name`,
                `last_check_in` - agent checkin, `model`, `platform`,
                `os_version`, `serial_number`, `user`

                Prepending a dash (-) to the parameter value will reverse
                the order of the returned results.

                Multiple values can be combined in a comma separated list
                to further customize the ordering of the response.
            os_version (str, optional): Return all device records with the specified OS version.
            platform (str, optional): Platform.
                Possible values: `Mac`, `iPad`, `iPhone`, `AppleTV`
            serial_number (str, optional): Serial Number
                If partial serial number is provided in the query,
                all device containing the partial string will be returned.
            user (str, optional): User name.
            user_email (str, optional): User email address.
            user_id (str, optional): User ID
            user_name (str, optional): Username
            limit (int, optional): Number of results to return per page. Defaults to 300.
            offset (int, optional): The initial index from which to return the results.

        Returns:
            list
        """
        params = {
            "asset_tag": asset_tag,
            "blueprint_id": blueprint_id,
            "device_id": device_id,
            "device_name": device_name,
            "mac_address": mac_address,
            "model": model,
            "ordering": ordering,
            "os_version": os_version,
            "platform": platform,
            "serial_number": serial_number,
            "user": user,
            "user_email": user_email,
            "user_id": user_id,
            "user_name": user_name,
            "limit": limit,
            "offset": offset,
        }

        return self._get("/devices", params=params)

    def get_device(self, id: str):
        """This request returns the high-level information for a specified Device ID.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}")

    def get_device_details(self, id):
        """This request returns the device details for a specified Device ID.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/details")

    def get_device_activity(self, id: str):
        """This request returns the device activity for a specified Device ID.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/activity")

    def get_device_apps(self, id: str):
        """This request returns a list of all installed apps for a specified Device ID.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/apps")

    def get_device_libraryitems(self, id: str):
        """This request gets all library items and their statuses for a specified Device ID

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/library-items")

    def get_device_parameters(self, id: str):
        """This request returns the parameters and their statuses for a specified Device ID

        This endpoint is only applicable to macOS clients.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/parameters")

    def get_device_status(self, id: str):
        """This request returns the full status (parameters and library items) for a specified Device ID.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/status")

    def list_device_notes(self, id: str):
        """This request gets all notes for the specified Device ID.

        Args:
            id (str): Device ID

        Returns:
            list
        """
        return self._get(f"/devices/{id}/notes")

    def get_device_note(self, device_id: str, note_id: str):
        """This request retrieves a specified note (Note ID) for the specified Device ID.

        Args:
            device_id (str): Device ID
            note_id (str): Note ID

        Returns:
            dict
        """
        return self._get(f"/devices/{device_id}/notes/{note_id}")

    def get_device_commands(self, id: str):
        """This endpoint sends a request to get information about the commands sent to a given device ID.

        MDM Status Codes
            1 : Command is Pending
            2 : Command is running
            3 : Command completed
            4 : Command failed
            5 : Command received "Not Now" response

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/commands")

    def get_device_bypasscode(self, id: str):
        """This request allows you to retrieve the Activation Lock Bypass code.

        `user_based_albc` is the user-based Activation Lock bypass code
        for when Activation Lock is enabled using an personal Apple ID and Find My.

        `device_based_albc` is the device-based Activation Lock bypass code
        for when Activation Lock is enabled by the MDM server.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/secrets/bypasscode")

    def get_device_filevaultkey(self, id: str):
        """This request allows you to retrieve the FileVault Recovery key for a macOS device.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/secrets/filevaultkey")

    def get_device_unlockpin(self, id: str):
        """This request allows you to retrieve the device unlock pin for a macOS device.

        Args:
            id (str): Device ID

        Returns:
            dict
        """
        return self._get(f"/devices/{id}/secrets/unlockpin")
