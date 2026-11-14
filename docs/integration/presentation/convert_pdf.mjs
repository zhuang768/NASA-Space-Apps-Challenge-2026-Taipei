/** Convert the validated PPTX, using actual local CJK fonts. No scientific changes. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
const root=process.cwd(),tmp=path.join(root,'.presentation-build');
const fontConfig=path.join(tmp,'fonts.conf');
await fs.writeFile(fontConfig,`<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"><fontconfig><dir>/Library/Fonts</dir><dir>/System/Library/Fonts</dir><dir>/System/Library/Fonts/Supplemental</dir><cachedir>${tmp}/font-cache</cachedir></fontconfig>`);
const bin=process.env.SOFFICE??'soffice';
execFileSync(bin,[`-env:UserInstallation=file://${tmp}/lo-profile-final`,'--headless','--convert-to','pdf','--outdir',path.join(root,'outputs/integration/presentation'),path.join(root,'outputs/integration/presentation/team_zasa_research.pptx')],{env:{...process.env,FONTCONFIG_FILE:process.env.FONTCONFIG_FILE??fontConfig},stdio:'inherit'});
