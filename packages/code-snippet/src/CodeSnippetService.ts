/*
 * 
 * This program is an unpublished work fully protected by the United States
 * copyright laws and is considered a trade secret belonging to Attala Systems Corporation.
 * To the extent that this work may be considered "published", the following notice applies
 * "(C) 2020, 2021, Attala Systems Corporation"
 *
 * Any unauthorized use, reproduction, distribution, display, modification,
 * or disclosure of this program is strictly prohibited.
 *
 */

import { IMetadata } from '@elyra/metadata-common';
import { MetadataService } from '@elyra/services';

import { Dialog, showDialog } from '@jupyterlab/apputils';

export const CODE_SNIPPET_SCHEMASPACE = 'code-snippets';
export const CODE_SNIPPET_SCHEMA = 'code-snippet';

export class CodeSnippetService {
  static async findAll(): Promise<IMetadata[]> {
    return MetadataService.getMetadata(CODE_SNIPPET_SCHEMASPACE);
  }

  // TODO: Test this function
  static async findByLanguage(language: string): Promise<IMetadata[]> {
    try {
      const allCodeSnippets: IMetadata[] = await this.findAll();
      const codeSnippetsByLanguage: IMetadata[] = [];

      for (const codeSnippet of allCodeSnippets) {
        if (codeSnippet.metadata.language === language) {
          codeSnippetsByLanguage.push(codeSnippet);
        }
      }

      return codeSnippetsByLanguage;
    } catch (error) {
      return Promise.reject(error);
    }
  }

  /**
   * Opens a dialog to confirm that the given code snippet
   * should be deleted, then sends a delete request to the metadata server.
   *
   * @param codeSnippet: code snippet to be deleted
   *
   * @returns A boolean promise that is true if the dialog confirmed
   * the deletion, and false if the deletion was cancelled.
   */
  static deleteCodeSnippet(codeSnippet: IMetadata): Promise<boolean> {
    return showDialog({
      title: `Delete snippet '${codeSnippet.display_name}'?`,
      buttons: [Dialog.cancelButton(), Dialog.okButton()]
    }).then((result: any) => {
      // Do nothing if the cancel button is pressed
      if (result.button.accept) {
        return MetadataService.deleteMetadata(
          CODE_SNIPPET_SCHEMASPACE,
          codeSnippet.name
        ).then(() => true);
      } else {
        return false;
      }
    });
  }
}
