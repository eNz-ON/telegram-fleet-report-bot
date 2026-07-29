from __future__ import annotations
from app.services.google_sheets import GoogleSheetsRepository
class FleetService:
    DRIVER_SHEETS=("CITI","Toyoty","skutery"); COMPANY_SHEETS=("spółki","Spółki","spolki","SPOLKI")
    def __init__(self, repository: GoogleSheetsRepository) -> None: self._repository=repository
    def find_driver(self, plate: str) -> str | None:
        p=plate.strip().lower()
        for sheet in self.DRIVER_SHEETS:
            for row in self._repository.get_rows(sheet)[1:]:
                if len(row)>5 and row[5].strip().lower()!="zakończony" and row[2].strip().lower()==p:
                    return f"👤 {row[0]}\n📞 {row[1]}"
        return None
    def find_vehicle(self, plate: str) -> str | None:
        p=plate.strip().lower()
        for row in self._repository.get_rows("flota")[1:]:
            if row and row[0].strip().lower()==p:
                v={"vin":self._v(row,1),"company":self._v(row,2),"model":self._v(row,3),"brand":self._v(row,4),"policy_number":self._v(row,5),"policy_name":self._v(row,6),"policy_date":self._v(row,7)}
                return self._format_vehicle(plate,v,self._find_company(v["company"]))
        return None
    def _find_company(self, key: str) -> dict[str,str]:
        rows=self._repository.find_existing_worksheet(self.COMPANY_SHEETS)
        if not rows: return {}
        k=key.strip().lower()
        for row in rows[1:]:
            if len(row)>1 and row[1].strip().lower()==k:
                return {"name":self._v(row,0),"krs":self._v(row,2),"nip":self._v(row,3),"regon":self._v(row,4),"address":self._v(row,5)}
        return {}
    @staticmethod
    def _v(row:list[str],i:int)->str: return row[i].strip() if len(row)>i else ""
    @staticmethod
    def _format_vehicle(plate:str,v:dict[str,str],c:dict[str,str])->str:
        line="──────────────"; parts=[f"🚗 {plate.strip().upper()}","",line,"📌 POJAZD",line,f"VIN: {v['vin']}",f"Model: {v['model']}",f"Marka: {v['brand']}"]
        if any(v[k] for k in ("policy_number","policy_name","policy_date")):
            parts += ["",line,"🛡️ POLISA",line]
            if v["policy_number"]: parts.append(f"Nr polisy: {v['policy_number']}")
            if v["policy_name"]: parts.append(f"Nazwa polisy: {v['policy_name']}")
            if v["policy_date"]: parts.append(f"Data polisy: {v['policy_date']}")
        if c.get("name"):
            parts += ["",line,"🏢 SPÓŁKA",line,c["name"],""]
            for label,key in (("KRS","krs"),("NIP","nip"),("REGON","regon")):
                if c.get(key): parts.append(f"{label}: {c[key]}")
        if c.get("address"): parts += ["",f"📍 {c['address']}"]
        return "\n".join(parts)
